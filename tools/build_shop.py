"""Build the read-only shop copy from the artifact HTML.
Usage: python3 build_shop.py <artifact.html> <photo-dir> <out-dir>
photo-dir holds <blobid>.jpg files; /_blob/<id> links become photos/<id>.jpg"""
import re,sys,os,shutil,json
src,pdir,out=sys.argv[1:4]
s=open(src,encoding='utf-8').read()
# strip publish skeleton if present
if s.lstrip().lower().startswith('<!doctype'):
    a=s.index('<body>')+6; b=s.rindex('</body>'); body=s[a:b]
else: body=s
os.makedirs(out+'/photos',exist_ok=True)
ids=set(re.findall(r'/_blob/([0-9a-f]{32})',body))
missing=[i for i in ids if not os.path.exists(f'{pdir}/{i}.jpg')]
if missing: sys.exit('missing photos: '+', '.join(missing))
for i in ids: shutil.copy(f'{pdir}/{i}.jpg',f'{out}/photos/{i}.jpg')
body=re.sub(r'/_blob/([0-9a-f]{32})',r'photos/\1.jpg',body)
# read-only footer note
body=body.replace("If a customer has a severe allergy, check the product label and tell them about shared equipment.",
 "If a customer has a severe allergy, check the product label and tell them about shared equipment. Read-only copy for shops.")
reset=":root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}"
head=('<!doctype html><html lang="en"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
 '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Allergens">'
 '<meta name="robots" content="noindex">'
 f'<style>{reset}</style></head><body>')
open(out+'/index.html','w',encoding='utf-8').write(head+body+'</body></html>')
open(out+'/.nojekyll','w').close()
print(len(ids),'photos;',os.path.getsize(out+'/index.html')//1024,'KB html')
