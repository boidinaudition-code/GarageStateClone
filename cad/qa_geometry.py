#!/usr/bin/env python3
"""Contrôles géométriques de la V2, à lancer après import_vendor_archives.py."""
from pathlib import Path
import json
import cadquery as cq
import trimesh
import generate_cad as g

ROOT=Path(__file__).resolve().parent
report={'parts':{},'reference_bounds_mm':{},'intersections_mm3':{},'stls':{}}
for name,part in g.PRINTABLE.items():
 bb=part.BoundingBox()
 report['parts'][name]={'valid':part.isValid(),'solids':len(part.Solids()),'bbox':[round(getattr(bb,k),3) for k in ('xmin','xmax','ymin','ymax','zmin','zmax')]}
 if not part.isValid() or len(part.Solids())!=1:raise AssertionError('Printable invalid: '+name)
 f=ROOT/'stl'/(name+'.stl')
 if f.is_file():
  m=trimesh.load_mesh(str(f))
  report['stls'][name]={'watertight':bool(m.is_watertight),'volume':bool(m.is_volume),'faces':len(m.faces)}
  if not m.is_watertight or not m.is_volume:raise AssertionError('STL not closed: '+name)
for name,part in g.REFERENCES.items():
 bb=part.BoundingBox()
 report['reference_bounds_mm'][name]=[round(getattr(bb,k),3) for k in ('xmin','xmax','ymin','ymax','zmin','zmax')]
def common_volume(a,b):
 aa=a.BoundingBox();bb=b.BoundingBox()
 if aa.xmax<=bb.xmin or aa.xmin>=bb.xmax or aa.ymax<=bb.ymin or aa.ymin>=bb.ymax or aa.zmax<=bb.zmin or aa.zmin>=bb.zmax:return 0.0
 return round(a.intersect(b).Volume(),5)
servo=next((v for k,v in g.REFERENCES.items() if 'MG90' in k),None)
if servo is None:print('ATTENTION: STEP servo absent, collision exacte non testee')
else:
 for name,shape in [('coque',g.shell),('toit',g.roof_lid),('support',g.cradle),('porte',g.door)]:
  volume=common_volume(servo,shape)
  report['intersections_mm3']['servo/'+name]=volume
  if volume>0.02:raise AssertionError('Collision servo/'+name+': '+str(volume))
xiao=next((v for k,v in g.REFERENCES.items() if 'XIAO' in k),None)
wio=next((v for k,v in g.REFERENCES.items() if 'WIO' in k),None)
if xiao is not None and wio is not None:
 report['intersections_mm3']['xiao/wio']=common_volume(xiao,wio)
report['warning']='Test numerique, aucune validation mecanique ou de fonctionnement physique. Le MG90-A peut differer du servo achete.'
(ROOT/'qa_report_runtime.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print('OK',len(report['parts']),'pieces STL; report -> cad/qa_report_runtime.json')
