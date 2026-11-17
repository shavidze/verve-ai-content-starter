import argparse, json
from pathlib import Path
from common import probe, read_json, resolve
p=argparse.ArgumentParser();p.add_argument('plan');a=p.parse_args()
plan=read_json(a.plan);target=resolve(plan['output'])
expected=sum(float(x['end'])-float(x['start']) for x in plan['segments'])
result={'video':str(target),'status':'FAIL','checks':{},'human_review_required':['Check faces and safe crop','Check Georgian subtitle spelling/timing','Check brand accuracy and treatment claims','Confirm explicit subject and owner permissions','Confirm any music and stock asset licensing']}
if not target.exists():
    result['checks']['output_exists']=False
else:
    v=probe(target)
    result['checks']={'output_exists':True,'vertical_1080x1920':v['width']==1080 and v['height']==1920,
        'duration_matches_plan':abs(v['duration']-expected)<0.5,'has_audio':v['has_audio'],
        'duration_seconds':v['duration']}
    if all(result['checks'][x] for x in ['output_exists','vertical_1080x1920','duration_matches_plan','has_audio']):
        result['status']='TECH_PASS_NEEDS_HUMAN_REVIEW'
print(json.dumps(result,ensure_ascii=False,indent=2))
report=target.parent/'quality-report.json';report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
if result['status']=='FAIL': raise SystemExit(1)
