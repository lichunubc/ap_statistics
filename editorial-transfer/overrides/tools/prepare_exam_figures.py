"""Build checked released-question crops; source PDFs stay in memory only."""
from pathlib import Path
import hashlib,json,urllib.request,time
ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'project/released-exam-figures.json'
PROVENANCE=ROOT/'project/released-exam-figures-provenance.json'
spec=json.loads(CONFIG.read_text())
old=json.loads(PROVENANCE.read_text()) if PROVENANCE.exists() else {'items':{}}
cache={};records={}
for item in spec['items']:
    path=ROOT/item['output'];key=item['id']
    signature=hashlib.sha256(json.dumps(item,sort_keys=True).encode()).hexdigest()
    record=old['items'].get(key,{})
    if path.exists() and record.get('spec_sha256')==signature and hashlib.sha256(path.read_bytes()).hexdigest()==record.get('image_sha256'):
        records[key]=record;continue
    import fitz
    url=item['source_url']
    assert url.startswith(('https://apcentral.collegeboard.org/','https://apstudents.collegeboard.org/','https://apclassroom.collegeboard.org/video-resources/'))
    if url not in cache:
        for attempt in range(3):
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'MapleHillSchool-Course-Figure-Builder/1.0'})
                with urllib.request.urlopen(req,timeout=60) as response:raw=response.read(20_000_001)
                if not raw.startswith(b'%PDF') or len(raw)>20_000_000:raise ValueError('Expected a public PDF: '+url)
                cache[url]=raw;break
            except Exception:
                if attempt==2:raise
                time.sleep(2*(attempt+1))
    raw=cache[url]
    doc=fitz.open(stream=raw,filetype='pdf');page=doc[item['pdf_page_index']]
    assert item['required_page_text'].casefold() in page.get_text().casefold(),f'Page identification failed: {key}'
    clip=fitz.Rect(item['clip_points']);assert page.rect.contains(clip),key
    pix=page.get_pixmap(matrix=fitz.Matrix(spec['render']['scale'],spec['render']['scale']),clip=clip,colorspace=fitz.csGRAY,alpha=False)
    path.parent.mkdir(parents=True,exist_ok=True);pix.save(path)
    records[key]={'source_url':url,'pdf_sha256':hashlib.sha256(raw).hexdigest(),'pdf_page_index':item['pdf_page_index'],'clip_points':item['clip_points'],'spec_sha256':signature,'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'width':pix.width,'height':pix.height,'renderer':f'PyMuPDF {fitz.VersionBind}','output':item['output']}
    doc.close()
PROVENANCE.write_text(json.dumps({'schema_version':1,'permission':spec['permission'],'items':records},ensure_ascii=False,indent=2)+'\n')
print(f'Verified {len(records)} released-question images; source PDFs not stored.')
