from pathlib import Path
import json, html

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'/'fluxwalls'
BASE='https://thobg01.github.io/Wallpapers/fluxwalls/'

def esc(x): return html.escape(str(x),quote=True)

def card(e,prefix=''):
    return f'<a class="card" href="{prefix}w/{e["slug"]}.html"><img loading="lazy" src="{prefix}assets/{e["asset"]}" alt="{esc(e["title"])}"><b>{esc(e["title"])}</b><small>{esc(e["orientation"])} · {e["width"]}×{e["height"]}</small></a>'

def collection(title,desc,items,canonical):
    cards=''.join(card(e,'../') for e in items)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} — FluxWalls</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><style>*{{box-sizing:border-box}}body{{margin:0;background:#090b10;color:#f5f7fa;font:16px/1.5 system-ui}}main{{width:min(1150px,calc(100% - 28px));margin:45px auto}}a{{color:inherit}}h1{{font-size:clamp(2.3rem,6vw,4.8rem);line-height:1;letter-spacing:-.05em}}p{{color:#aab3c0;max-width:720px}}.nav{{display:flex;gap:14px;flex-wrap:wrap;margin:25px 0}}.nav a{{color:#8de8c1}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}.card{{text-decoration:none;background:#11151c;border:1px solid #252c37;border-radius:16px;padding:9px}}.card img{{width:100%;height:260px;object-fit:cover;border-radius:10px;display:block;margin-bottom:9px}}.card b,.card small{{display:block}}.card small{{color:#929dad;margin-top:3px}}@media(max-width:850px){{.grid{{grid-template-columns:repeat(3,1fr)}}}}@media(max-width:600px){{.grid{{grid-template-columns:repeat(2,1fr)}}.card img{{height:220px}}}}</style></head><body><main><a href="../">← FluxWalls</a><h1>{esc(title)}</h1><p>{esc(desc)}</p><div class="nav"><a href="mobile.html">Phone wallpapers</a><a href="desktop.html">Desktop wallpapers</a><a href="square.html">Square wallpapers</a></div><section class="grid">{cards}</section></main></body></html>'''

def main():
    catalog=json.loads((OUT/'catalog.json').read_text(encoding='utf-8'))
    cdir=OUT/'collections'; cdir.mkdir(exist_ok=True)
    specs={
      'mobile':('Free Phone Wallpapers','Original vertical abstract wallpapers sized for modern phone screens.'),
      'desktop':('Free Desktop Wallpapers','Original widescreen abstract wallpapers for desktop and laptop displays.'),
      'square':('Free Square Wallpapers','Original square abstract backgrounds for profiles, covers and square displays.')}
    urls=[]
    for key,(title,desc) in specs.items():
        items=[e for e in catalog if e['orientation']==key]
        url=BASE+'collections/'+key+'.html'; urls.append(url)
        (cdir/(key+'.html')).write_text(collection(title,desc,items[:120],url),encoding='utf-8')
    families=sorted({e['family'] for e in catalog})
    for fam in families:
        items=[e for e in catalog if e['family']==fam]
        title=f'{fam.title()} Abstract Wallpapers'; desc=f'Free original {fam} style abstract wallpapers for phones and desktops.'
        url=BASE+'collections/'+fam+'.html'; urls.append(url)
        (cdir/(fam+'.html')).write_text(collection(title,desc,items[:120],url),encoding='utf-8')
    idx=OUT/'index.html'; s=idx.read_text(encoding='utf-8')
    nav='<div style="display:flex;gap:12px;flex-wrap:wrap;margin:0 0 28px"><a href="collections/mobile.html">Phone</a><a href="collections/desktop.html">Desktop</a><a href="collections/square.html">Square</a>'+''.join(f'<a href="collections/{f}.html">{f.title()}</a>' for f in families)+'</div>'
    if 'collections/mobile.html' not in s: s=s.replace('<section class="grid">',nav+'<section class="grid">',1)
    idx.write_text(s,encoding='utf-8')
    pages=OUT/'w'
    for i,e in enumerate(catalog):
        p=pages/(e['slug']+'.html')
        if not p.exists(): continue
        s=p.read_text(encoding='utf-8')
        if 'More wallpapers' in s: continue
        related=[x for x in catalog if x['slug']!=e['slug'] and (x['family']==e['family'] or x['orientation']==e['orientation'])][:6]
        links='<section class="w" style="padding:10px 0 55px"><h2>More wallpapers</h2><p>'+f'<a href="../collections/{e["orientation"]}.html">More {esc(e["orientation"])} wallpapers</a> · <a href="../collections/{e["family"]}.html">More {esc(e["family"])} designs</a></p><div style="display:flex;gap:10px;flex-wrap:wrap">'+''.join(f'<a href="{x["slug"]}.html">{esc(x["title"])}</a>' for x in related)+'</div></section>'
        s=s.replace('</main>',links+'</main>',1)
        p.write_text(s,encoding='utf-8')
    sm=OUT/'sitemap.xml'; s=sm.read_text(encoding='utf-8')
    for u in urls:
        if u not in s: s=s.replace('</urlset>',f'<url><loc>{u}</loc></url>\n</urlset>')
    sm.write_text(s,encoding='utf-8')
    print('Enhanced',len(catalog),'wallpapers and',len(urls),'collection pages')
if __name__=='__main__': main()
