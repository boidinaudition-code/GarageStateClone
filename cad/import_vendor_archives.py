#!/usr/bin/env python3
"""Extrait sans risque les quatre STEP du projet (ne decompresse pas d'autres membres)."""
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
import sys
MAPPING={
 'servo':('dms-mg90-a-1.snapshot.4.zip','Mg90.STEP'),
 'transistor':('transistor-bc547-b-1.snapshot.7.zip','BC547-B.step'),
 'wio':('wio-sx1262-for-xiao-1.snapshot.4.zip','Wio-SX1262_for_XIAO_3D_file V2.step'),
 'xiao':('seeed-studio-xiao-nrf52840-1.snapshot.2.zip','XIAO-nRF52840  v3.step'),
}
def main(folder):
 out=Path(__file__).resolve().parent/'refs'
 out.mkdir(exist_ok=True)
 for name,(archive,member) in MAPPING.items():
  path=folder/archive
  with ZipFile(path) as z:
   data=z.read(member)
  if not data.startswith(b'ISO-10303-21;'): raise ValueError('En-tete STEP non reconnu: '+archive)
  target=out/(name+'.step')
  target.write_bytes(data)
  print(name,len(data),sha256(data).hexdigest(),str(target))
 print("Lancer ensuite python generate_cad.py")
if __name__=='__main__':
 main(Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve())
