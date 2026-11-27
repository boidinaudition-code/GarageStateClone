// Garage miniature LoRa — prototype 1.0
// 2 x Seeed XIAO nRF52840 + Wio-SX1262 (SKU 102010710)
// Programmation PlatformIO : env:emetteur OU env:recepteur.
// Usage : simple retour d'etat, ne commande PAS la porte reelle.

#include <Arduino.h>
#include <Adafruit_TinyUSB.h>
#include <SPI.h>
#include <RadioLib.h>

#if defined(ROLE_RECEPTEUR)
  #include <Servo.h>
#endif

#if defined(ROLE_EMETTEUR) == defined(ROLE_RECEPTEUR)
  #error "Choisir UNE configuration : emetteur ou recepteur."
#endif

// Wio-SX1262 for XIAO (headers 2x7, pas version B2B ESP32-S3)
static constexpr int PIN_LORA_NSS   = D4;
static constexpr int PIN_LORA_DIO1  = D1;
static constexpr int PIN_LORA_RST   = D2;
static constexpr int PIN_LORA_BUSY  = D3;
static constexpr int PIN_LORA_RFSW  = D5;

// IMPORTANT: D5 HIGH active le controle du commutateur RF par DIO2.
SX1262 radio = new Module(PIN_LORA_NSS, PIN_LORA_DIO1,
                          PIN_LORA_RST, PIN_LORA_BUSY);

// Valeurs IDENTIQUES sur les deux cartes.
static constexpr float    RADIO_MHZ = 868.125f;
static constexpr float    RADIO_BW_KHZ = 125.0f;
static constexpr uint8_t  RADIO_SF = 8;
static constexpr uint8_t  RADIO_CR = 5; // 4/5 selon RadioLib
static constexpr int8_t   RADIO_TX_DBM = 10;
static constexpr uint8_t  RADIO_SYNC = 0x12;
static constexpr float    RADIO_TCXO_V = 1.8f;

static constexpr uint16_t NETWORK_ID = 0x6A93;
static constexpr uint8_t PROTOCOL_VERSION = 1;
static constexpr uint8_t KIND_STATUS = 0x53; // S
static constexpr uint8_t KIND_ACK = 0x41;    // A

static constexpr uint8_t STATE_CLOSED = 0;
static constexpr uint8_t STATE_OPEN = 1;
static constexpr uint8_t STATE_MIDDLE = 2;
static constexpr uint8_t STATE_SENSOR_FAULT = 3;

// Format fixe (8 octets) : la protection contre erreurs radio est le CRC LoRa.
// NETWORK_ID filtre uniquement les trames d'autres projets, sans authentification.
struct __attribute__((packed)) Frame {
  uint16_t network;
  uint8_t version;
  uint8_t kind;
  uint16_t sequence;
  uint8_t value;
  uint8_t reserved;
};
static_assert(sizeof(Frame) == 8, "Trame attendue sur 8 octets");

volatile bool radioFlag = false;
void onRadioIRQ() { radioFlag = true; }

bool consumeRadioIRQ() {
  noInterrupts();
  bool flag = radioFlag;
  radioFlag = false;
  interrupts();
  return flag;
}

bool validFrame(const Frame& f, uint8_t kind) {
  return f.network == NETWORK_ID && f.version == PROTOCOL_VERSION &&
         f.kind == kind;
}

void fatalRadio(const char* context, int16_t code) {
  Serial.print("ERREUR RADIO ");
  Serial.print(context);
  Serial.print(" = ");
  Serial.println(code);
  while (true) delay(1000);
}

void initRadio() {
  pinMode(PIN_LORA_RFSW, OUTPUT);
  digitalWrite(PIN_LORA_RFSW, HIGH);
  SPI.begin();

  int16_t result = radio.begin(RADIO_MHZ, RADIO_BW_KHZ, RADIO_SF,
                               RADIO_CR, RADIO_SYNC, RADIO_TX_DBM,
                               8, RADIO_TCXO_V, false);
  if (result != RADIOLIB_ERR_NONE) fatalRadio("init", result);

  result = radio.setDio2AsRfSwitch(true);
  if (result != RADIOLIB_ERR_NONE) fatalRadio("DIO2 RF switch", result);

  radio.setDio1Action(onRadioIRQ);
  Serial.println("SX1262 initialisee : 868.125 MHz / SF8 / 125 kHz / 10 dBm");
}

Frame makeFrame(uint8_t kind, uint16_t seq, uint8_t value) {
  Frame f{};
  f.network = NETWORK_ID;
  f.version = PROTOCOL_VERSION;
  f.kind = kind;
  f.sequence = seq;
  f.value = value;
  return f;
}

#if defined(ROLE_EMETTEUR)

static constexpr uint8_t PIN_CLOSED = D6;
static constexpr uint8_t PIN_OPEN = D7; // utiliser seulement avec OPEN_SENSOR_PRESENT=1
#if !OPEN_SENSOR_PRESENT
  #ifndef SINGLE_SENSOR_OPEN_ESTIMATE_MS
    #define SINGLE_SENSOR_OPEN_ESTIMATE_MS 40000UL
  #endif
#endif
static constexpr uint32_t DEBOUNCE_MS = 150;
static constexpr uint32_t HEARTBEAT_MS = 60000; // duree entre deux rapports
static constexpr uint32_t ACK_WAIT_MS = 600;
static constexpr uint32_t RETRY_PAUSE_MS = 250;

uint8_t stableState = STATE_MIDDLE;
uint8_t candidateState = STATE_MIDDLE;
uint32_t candidateSince = 0;
uint32_t lastReportMs = 0;
uint16_t seqCounter = 0;
bool reportPending = true; // envoyer l'etat immediatement au demarrage
#if !OPEN_SENSOR_PRESENT
uint32_t absenceMagnetSince = 0; // depart du delai d'ouverture ESTIMEE, pas mesuree
#endif

uint8_t readDoor() {
  // Contact sec SAS308 qui se FERME quand l'aimant arrive en fin de course.
  const bool atClosed = (digitalRead(PIN_CLOSED) == LOW);
  #if OPEN_SENSOR_PRESENT
  const bool atOpen = (digitalRead(PIN_OPEN) == LOW);
  #else
  const bool atOpen = false;
  #endif

  if (atClosed && atOpen) return STATE_SENSOR_FAULT;
  if (atClosed) return STATE_CLOSED;
  if (atOpen) return STATE_OPEN;
  return STATE_MIDDLE; // ni ouvert complet ni ferme complet
}

bool transmitWithAck(uint8_t doorState) {
  const uint16_t sequence = ++seqCounter;
  Frame frame = makeFrame(KIND_STATUS, sequence, doorState);

  for (int attempt = 1; attempt <= 3; ++attempt) {
    consumeRadioIRQ();
    int16_t rc = radio.transmit(reinterpret_cast<uint8_t*>(&frame),
                                sizeof(frame));
    if (rc != RADIOLIB_ERR_NONE) {
      Serial.print("TX erreur = "); Serial.println(rc);
      delay(RETRY_PAUSE_MS);
      continue;
    }

    // Le recepteur temporise son ACK pour nous laisser passer en RX.
    consumeRadioIRQ();
    rc = radio.startReceive();
    if (rc != RADIOLIB_ERR_NONE) {
      Serial.print("RX erreur = "); Serial.println(rc);
      delay(RETRY_PAUSE_MS);
      continue;
    }

    const uint32_t start = millis();
    while (millis() - start < ACK_WAIT_MS) {
      if (consumeRadioIRQ()) {
        Frame answer{};
        const size_t n = radio.getPacketLength();
        if (n == sizeof(answer) &&
            radio.readData(reinterpret_cast<uint8_t*>(&answer),
                           sizeof(answer)) == RADIOLIB_ERR_NONE &&
            validFrame(answer, KIND_ACK) &&
            answer.sequence == sequence) {
          Serial.print("ACK #"); Serial.print(sequence);
          Serial.print(" RSSI = "); Serial.println(radio.getRSSI());
          radio.standby();
          return true;
        }
        // En cas de trame differente, reprendre la reception d'ACK.
        radio.startReceive();
      }
      delay(2);
    }

    radio.standby();
    Serial.print("ACK absent, tentative "); Serial.println(attempt);
    if (attempt < 3) delay(RETRY_PAUSE_MS);
  }
  return false;
}

void setup() {
  Serial.begin(115200);
  delay(350);
  Serial.println("GARAGE REEL : EMETTEUR");
  pinMode(PIN_CLOSED, INPUT_PULLUP);
  #if OPEN_SENSOR_PRESENT
  pinMode(PIN_OPEN, INPUT_PULLUP);
  #endif
  delay(200); // stabilisation contacts au demarrage
  stableState = candidateState = readDoor();
  candidateSince = millis();
#if !OPEN_SENSOR_PRESENT
  absenceMagnetSince = candidateSince;
  Serial.println("Capteur unique FERME : ouverture inferee apres delai, PAS confirmee");
#endif
  initRadio();
}

void loop() {
  const uint32_t now = millis();
  uint8_t raw = readDoor();
#if !OPEN_SENSOR_PRESENT
  if (raw == STATE_CLOSED) {
    // Aimant en face = fermeture vraiment constatee.
    absenceMagnetSince = now;
  } else if (now - absenceMagnetSince >= SINGLE_SENSOR_OPEN_ESTIMATE_MS) {
    // Une seule fin de course NE PROUVE JAMAIS la pleine ouverture.
    // Heuristique purement decorative pour animer la porte/LED miniature.
    raw = STATE_OPEN;
  }
#endif
  if (raw != candidateState) {
    candidateState = raw;
    candidateSince = now;
  }
  if (candidateState != stableState && now - candidateSince >= DEBOUNCE_MS) {
    stableState = candidateState;
    reportPending = true;
    Serial.print("Etat detecte = "); Serial.println(stableState);
  }

  if (reportPending || now - lastReportMs >= HEARTBEAT_MS) {
    // IMPORTANT : aucune boucle de transmission continue si la liaison est absente.
    reportPending = false;
    const bool ack = transmitWithAck(stableState);
    lastReportMs = millis();
    Serial.println(ack ? "Etat confirme" : "Etat envoye sans confirmation");
  }
  delay(10);
}

#else  // ROLE_RECEPTEUR

static constexpr uint8_t PIN_SERVO = D6;
static constexpr uint8_t PIN_INTERIOR_LED = D7; // base BC547B via 4.7k ; LED blanche +5V ; active HIGH
static constexpr uint8_t PIN_AMBER_LED = D0;    // orange facade, active LOW (absorption)
static constexpr uint32_t LINK_TIMEOUT_MS = 150000;
static constexpr uint8_t ANGLE_CLOSED = 90; // porte verticale (sens inverse)
static constexpr uint8_t ANGLE_OPEN = 0;    // porte horizontale
static constexpr uint32_t OPEN_TRAVEL_MS = 5000;
static constexpr uint32_t CLOSE_TRAVEL_MS = 5000;
static_assert(ANGLE_OPEN != ANGLE_CLOSED && ANGLE_OPEN <= 180 && ANGLE_CLOSED <= 180,
              "Angles servo distincts entre 0 et 180 degres");
static constexpr uint8_t FULL_TRAVEL_DEG = ANGLE_OPEN > ANGLE_CLOSED
    ? ANGLE_OPEN - ANGLE_CLOSED : ANGLE_CLOSED - ANGLE_OPEN;


Servo doorServo;
uint8_t currentAngle = ANGLE_CLOSED;
uint8_t targetAngle = ANGLE_CLOSED;
bool servoStarted = false;
bool haveStatus = false;
uint8_t receivedDoorState = STATE_MIDDLE;
uint32_t lastValidFrameMs = 0;
uint8_t motionStartAngle = ANGLE_CLOSED;
uint32_t motionStartMs = 0;
uint32_t motionDurationMs = 0;

void animateServo(uint32_t now) {
  if (!servoStarted || currentAngle == targetAngle) return;
  const uint32_t elapsed = now - motionStartMs;
  const uint8_t distance = targetAngle > motionStartAngle
      ? targetAngle - motionStartAngle : motionStartAngle - targetAngle;
  const uint8_t steps = elapsed >= motionDurationMs
      ? distance : (elapsed * distance) / motionDurationMs;
  const uint8_t nextAngle = targetAngle > motionStartAngle
      ? motionStartAngle + steps : motionStartAngle - steps;
  if (nextAngle != currentAngle) {
    currentAngle = nextAngle;
    doorServo.write(currentAngle);
  }
}

void setTarget(uint8_t state) {
  receivedDoorState = state;
  uint8_t nextTarget;
  switch (state) {
    case STATE_CLOSED: nextTarget = ANGLE_CLOSED; break;
    // Capteur unique : NON FERME declenche directement l'ouverture decorative.
    // Le passage ulterieur MIDDLE -> OPEN ne doit pas relancer le mouvement.
    case STATE_OPEN:
    case STATE_MIDDLE: nextTarget = ANGLE_OPEN; break;
    default: return;
  }
  const uint32_t now = millis();
  if (!servoStarted) {
    doorServo.attach(PIN_SERVO);
    doorServo.write(currentAngle);
    servoStarted = true;
  }
  if (nextTarget == targetAngle) return;
  animateServo(now);
  motionStartAngle = currentAngle;
  targetAngle = nextTarget;
  motionStartMs = now;
  const uint8_t distance = targetAngle > currentAngle
      ? targetAngle - currentAngle : currentAngle - targetAngle;
  const uint32_t fullTravelMs = targetAngle == ANGLE_OPEN
      ? OPEN_TRAVEL_MS : CLOSE_TRAVEL_MS;
  // Duree proportionnelle au trajet restant lors d'une inversion en cours de route.
  motionDurationMs = (fullTravelMs * distance) / FULL_TRAVEL_DEG;
}

// Orange en absorption de courant : 3V3 -> 680 ohms -> anode LED -> cathode D0.
// Sortie LOW = allumee ; entree haute impedance = eteinte.
// Jamais OUTPUT HIGH, au cas ou D0 serait partage avec un bouton a la masse.
void setAmberLed(bool on) {
  if (on) {
    digitalWrite(PIN_AMBER_LED, LOW);
    pinMode(PIN_AMBER_LED, OUTPUT);
  } else {
    pinMode(PIN_AMBER_LED, INPUT);
  }
}

void updateLeds(uint32_t now) {
  const bool stale = !haveStatus || (now - lastValidFrameMs > LINK_TIMEOUT_MS);
  const bool servoMoving = servoStarted && currentAngle != targetAngle;
  const bool openRequested = receivedDoorState == STATE_OPEN || receivedDoorState == STATE_MIDDLE;
  const bool fullyOpen = !stale && openRequested && servoStarted && currentAngle == ANGLE_OPEN && !servoMoving;

  // D7 pilote la base du BC547B via 4.7k ; LED blanche sur +5V avec 330 ohms.
  digitalWrite(PIN_INTERIOR_LED, fullyOpen ? HIGH : LOW);

  bool amberOn = false;
  if (stale) {
    // Liaison perdue : 2 flashes rapproches toutes les 2 secondes.
    const uint32_t phase = now % 2000;
    amberOn = phase < 150 || (phase >= 300 && phase < 450);
  } else if (receivedDoorState == STATE_SENSOR_FAULT) {
    amberOn = (now % 200) < 100; // capteurs incoherents : 5 Hz
  } else if (servoMoving) {
    amberOn = (now % 500) < 250; // servo miniature en mouvement : 2 Hz
  } else {
    amberOn = openRequested; // ouverte estimee fixe, fermee eteinte
  }
  setAmberLed(amberOn);
}

void processRadio() {
  Frame frame{};
  const size_t n = radio.getPacketLength();
  const int16_t rc = (n == sizeof(frame))
     ? radio.readData(reinterpret_cast<uint8_t*>(&frame), sizeof(frame))
     : RADIOLIB_ERR_UNKNOWN;

  if (rc == RADIOLIB_ERR_NONE && validFrame(frame, KIND_STATUS) &&
      frame.value <= STATE_SENSOR_FAULT) {
    haveStatus = true;
    lastValidFrameMs = millis();
    setTarget(frame.value);

    Serial.print("Etat = "); Serial.print(frame.value);
    Serial.print(" seq = "); Serial.print(frame.sequence);
    Serial.print(" RSSI = "); Serial.println(radio.getRSSI());

    // Laisser le temps a l'emetteur de basculer de TX en RX.
    delay(50);
    Frame ack = makeFrame(KIND_ACK, frame.sequence, frame.value);
    int16_t tx = radio.transmit(reinterpret_cast<uint8_t*>(&ack), sizeof(ack));
    if (tx != RADIOLIB_ERR_NONE) {
      Serial.print("ACK TX erreur = "); Serial.println(tx);
    }
  }
  // Toujours revenir en ecoute, y compris apres une trame invalide.
  consumeRadioIRQ();
  int16_t rx = radio.startReceive();
  if (rx != RADIOLIB_ERR_NONE) Serial.println("Erreur retour RX");
}

void setup() {
  Serial.begin(115200);
  delay(350);
  Serial.println("GARAGE MINIATURE : RECEPTEUR");
  pinMode(PIN_INTERIOR_LED, OUTPUT);
  digitalWrite(PIN_INTERIOR_LED, LOW);
  pinMode(PIN_AMBER_LED, INPUT); // orange eteinte / haute impedance
  initRadio();
  const int16_t rx = radio.startReceive();
  if (rx != RADIOLIB_ERR_NONE) fatalRadio("startReceive", rx);
}

void loop() {
  if (consumeRadioIRQ()) processRadio();
  const uint32_t now = millis();
  animateServo(now);
  updateLeds(now);
  delay(2);
}

#endif
