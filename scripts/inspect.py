import argparse, json
from common import probe

p=argparse.ArgumentParser(description='Inspect video metadata with ffprobe')
p.add_argument('video')
a=p.parse_args()
print(json.dumps(probe(a.video),ensure_ascii=False,indent=2))
