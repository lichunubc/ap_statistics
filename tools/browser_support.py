"""Browser helpers: normal HTTP in CI; explicit no-network inlining for sandbox QA."""
from pathlib import Path
from urllib.parse import unquote
import base64, os, re
from bs4 import BeautifulSoup

def inline_javascript(path):
    path=Path(path)
    def dependency(m):
        source=(path.parent/m[2]).resolve()
        encoded=base64.b64encode(inline_javascript(source).encode()).decode()
        return m[1]+'"data:text/javascript;base64,'+encoded+'"'
    # The Quarto module imports tabsets relatively. Resolve that module offline,
    # preserving its behavior rather than suppressing framework JavaScript errors.
    return re.sub(r'(\bfrom\s+)["\'](\.[^"\']+)["\']',dependency,path.read_text())

def load_page(page,path,url):
    if not os.environ.get('INLINE_BROWSER'):
        page.goto(url,wait_until='networkidle');return
    path=Path(path);soup=BeautifulSoup(path.read_text(),'html.parser')
    for tag in soup.select('script[src]'):
        src=path.parent/unquote(tag['src']);tag.attrs.pop('src');tag.string=inline_javascript(src)
    for tag in soup.select('link[rel=stylesheet]'):
        src=path.parent/unquote(tag['href']);style=soup.new_tag('style');style.string=src.read_text();tag.replace_with(style)
    page.set_content(inline_document(soup),wait_until='load')

def inline_document(soup):
    # about:blank has an opaque origin in the restricted browser. Model the
    # framework's UI-only storage in memory; never persist quiz choices.
    tag=soup.new_tag('script')
    tag.string='''for (const key of ['localStorage','sessionStorage']) {
      const values=new Map(); Object.defineProperty(window,key,{configurable:true,value:{
        getItem:k=>values.has(String(k))?values.get(String(k)):null,
        setItem:(k,v)=>values.set(String(k),String(v)),removeItem:k=>values.delete(String(k)),
        clear:()=>values.clear(),key:i=>Array.from(values.keys())[i]??null,
        get length(){return values.size;}}});}'''
    soup.head.insert(0,tag)
    return str(soup)
