from urllib.request import urlopen
from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
meta=json.loads(urlopen('https://data.jsdelivr.com/v1/package/npm/@fontsource-variable/inter',timeout=15).read())
v=meta['tags']['latest'];base=f'https://cdn.jsdelivr.net/npm/@fontsource-variable/inter@{v}/'
for name,path in [('inter-latin.woff2','files/inter-latin-wght-normal.woff2'),('INTER-LICENSE.txt','LICENSE')]:
 data=urlopen(base+path,timeout=15).read();(root/'app/vendor'/name).write_bytes(data);print(base+path,len(data))
base='https://raw.githubusercontent.com/twbs/icons/v1.13.1/'
for name,path in [('leaf.svg','icons/leaf.svg'),('ICONS-LICENSE.txt','LICENSE')]:
 data=urlopen(base+path,timeout=15).read();(root/'app/vendor'/name).write_bytes(data);print(base+path,len(data))
