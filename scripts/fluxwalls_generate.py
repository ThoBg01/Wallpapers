from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from string import Template
import hashlib, html, json, math, random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "fluxwalls"
ASSETS = OUT / "assets"
PAGES = OUT / "w"
OUT.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)
PAGES.mkdir(parents=True, exist_ok=True)

BASE = "https://thobg01.github.io/Wallpapers/fluxwalls/"
ADS_CLIENT = "ca-pub-9886017981009232"
ADS_SLOT = "4586711336"
INDEXNOW_KEY = hashlib.sha256(b"fluxwalls-autonomous-indexnow-v1").hexdigest()[:32]

PALETTES = [
    ["#07111F","#113A5C","#53D8FB","#D6FFF6"],
    ["#120A1F","#3A176B","#FF4FD8","#FFB86B"],
    ["#081C15","#1B4332","#74C69D","#D8F3DC"],
    ["#0B0D17","#162447","#1F4068","#E43F5A"],
    ["#0F1020","#27296D","#5E63B6","#A393EB"],
    ["#110B11","#3A183A","#C85C8E","#F6C6EA"],
    ["#091A1A","#0B525B","#0B7A75","#9CEAEF"],
    ["#15100A","#513C2C","#B86F52","#FFD6A5"],
    ["#081018","#0A2463","#3E92CC","#FFF1D0"],
    ["#11131A","#232946","#B8C1EC","#EEBBC3"],
    ["#050505","#171717","#7C3AED","#22D3EE"],
    ["#101018","#28283A","#F59E0B","#FDE68A"],
]

FAMILIES = ["aurora","halo","waves","orbital","paper","mesh","dusk","neon"]
FORMATS = [
    ("mobile",1440,3200),("mobile",1440,3200),("mobile",1440,3200),("mobile",1440,3200),
    ("desktop",2560,1440),("desktop",2560,1440),("desktop",2560,1440),
    ("square",2048,2048),
]

def esc(x): return html.escape(str(x), quote=True)

def seed_for(day, i):
    return int(hashlib.sha256(f"{day}-{i}-fluxwalls".encode()).hexdigest()[:16], 16)

def path_wave(w, h, y, amp, phase):
    pts = []
    for i in range(9):
        x = w * i / 8
        yy = y + math.sin(i * 0.9 + phase) * amp
        pts.append((x, yy))
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    for j in range(1, len(pts)):
        x0,y0 = pts[j-1]
        x1,y1 = pts[j]
        cx = (x0+x1)/2
        d += f" Q {cx:.1f} {y0:.1f} {x1:.1f} {y1:.1f}"
    return d

def blob_path(cx, cy, rx, ry, rng):
    pts=[]
    n=8
    for i in range(n):
        a=2*math.pi*i/n
        r=0.72+rng.random()*0.42
        pts.append((cx+math.cos(a)*rx*r, cy+math.sin(a)*ry*r))
    d=f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        p=pts[i]
        q=pts[(i+1)%n]
        mx=(p[0]+q[0])/2
        my=(p[1]+q[1])/2
        d+=f" Q {p[0]:.1f} {p[1]:.1f} {mx:.1f} {my:.1f}"
    return d+" Z"

def make_svg(w, h, family, colors, rng):
    c0,c1,c2,c3=colors
    defs=f"""
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="{c0}"/><stop offset="52%" stop-color="{c1}"/><stop offset="100%" stop-color="{c0}"/>
      </linearGradient>
      <radialGradient id="r1"><stop offset="0%" stop-color="{c2}" stop-opacity=".95"/><stop offset="100%" stop-color="{c2}" stop-opacity="0"/></radialGradient>
      <radialGradient id="r2"><stop offset="0%" stop-color="{c3}" stop-opacity=".82"/><stop offset="100%" stop-color="{c3}" stop-opacity="0"/></radialGradient>
      <linearGradient id="g1" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{c2}"/><stop offset="1" stop-color="{c3}"/></linearGradient>
      <filter id="blur"><feGaussianBlur stdDeviation="{max(w,h)/38:.1f}"/></filter>
      <filter id="blur2"><feGaussianBlur stdDeviation="{max(w,h)/75:.1f}"/></filter>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="{rng.randint(1,999)}"/>
        <feColorMatrix type="saturate" values="0"/>
      </filter>
    </defs>"""
    parts=[f'<rect width="{w}" height="{h}" fill="url(#bg)"/>']
    if family=="aurora":
        for k in range(4):
            y=h*(.22+.18*k)+rng.uniform(-.08,.08)*h
            d=path_wave(w,h,y,h*.10,rng.random()*5)
            parts.append(f'<path d="{d}" fill="none" stroke="{c2 if k%2==0 else c3}" stroke-width="{h*.10:.0f}" stroke-linecap="round" opacity=".32" filter="url(#blur)"/>')
    elif family=="halo":
        cx=w*(.35+rng.random()*.3); cy=h*(.35+rng.random()*.3)
        for k in range(7):
            r=min(w,h)*(.11+k*.07)
            parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="none" stroke="{c2 if k%2==0 else c3}" stroke-width="{max(3,min(w,h)*.009):.0f}" opacity="{.62-k*.06:.2f}"/>')
        parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{min(w,h)*.28:.0f}" fill="url(#r1)" filter="url(#blur2)"/>')
    elif family=="waves":
        for k in range(9):
            y=h*(.12+k*.095)
            d=path_wave(w,h,y,h*.06,rng.random()*6)
            parts.append(f'<path d="{d}" fill="none" stroke="{c2 if k%2==0 else c3}" stroke-width="{max(4,h*.008):.0f}" opacity="{.18+.055*k:.2f}"/>')
    elif family=="orbital":
        cx=w*(.45+rng.random()*.1); cy=h*(.47+rng.random()*.08)
        parts.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{w*.36:.0f}" ry="{h*.19:.0f}" fill="none" stroke="{c3}" stroke-width="{max(4,w*.006):.0f}" opacity=".55" transform="rotate(-19 {cx:.0f} {cy:.0f})"/>')
        parts.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{w*.28:.0f}" ry="{h*.27:.0f}" fill="none" stroke="{c2}" stroke-width="{max(3,w*.004):.0f}" opacity=".42" transform="rotate(31 {cx:.0f} {cy:.0f})"/>')
        parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{min(w,h)*.24:.0f}" fill="url(#r1)"/>')
        parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{min(w,h)*.065:.0f}" fill="{c3}"/>')
    elif family=="paper":
        for k in range(7):
            cx=w*(.15+rng.random()*.7); cy=h*(.12+rng.random()*.76)
            d=blob_path(cx,cy,w*(.16+rng.random()*.16),h*(.10+rng.random()*.12),rng)
            parts.append(f'<path d="{d}" fill="{[c1,c2,c3][k%3]}" opacity="{.22+.07*k:.2f}" filter="url(#blur2)"/>')
    elif family=="mesh":
        for k in range(10):
            cx=rng.random()*w; cy=rng.random()*h; r=min(w,h)*(.12+rng.random()*.22)
            parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#{["r1","r2"][k%2]})" filter="url(#blur2)" opacity=".75"/>')
    elif family=="dusk":
        for k in range(6):
            cy=h*(.64+k*.065)
            d=f"M 0 {cy:.0f} Q {w*.25:.0f} {cy-h*.09:.0f} {w*.5:.0f} {cy:.0f} T {w:.0f} {cy:.0f} L {w} {h} L 0 {h} Z"
            parts.append(f'<path d="{d}" fill="{[c1,c2,c0][k%3]}" opacity="{.22+.08*k:.2f}"/>')
        parts.append(f'<circle cx="{w*.72:.0f}" cy="{h*.26:.0f}" r="{min(w,h)*.11:.0f}" fill="{c3}" opacity=".82" filter="url(#blur2)"/>')
    else:
        for k in range(14):
            x=rng.uniform(-.1,.9)*w; y=rng.uniform(-.05,.95)*h
            ww=w*(.015+rng.random()*.06); hh=h*(.20+rng.random()*.42)
            rot=rng.uniform(-35,35)
            parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{ww:.0f}" height="{hh:.0f}" rx="{ww*.45:.0f}" fill="{c2 if k%2==0 else c3}" opacity="{.10+rng.random()*.33:.2f}" transform="rotate({rot:.1f} {x:.0f} {y:.0f})" filter="url(#blur2)"/>')
    parts.append(f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".045" style="mix-blend-mode:soft-light"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{defs}{"".join(parts)}</svg>'

DETAIL = Template("""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>$title — FluxWalls</title><meta name="description" content="$description">
<meta name="robots" content="index,follow"><link rel="canonical" href="$canonical"><meta name="theme-color" content="#090b10">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=$ads_client" crossorigin="anonymous"></script>
<style>
*{box-sizing:border-box}body{margin:0;background:#090b10;color:#f6f7fb;font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}a{color:inherit}.w{width:min(1100px,calc(100% - 28px));margin:auto}nav{border-bottom:1px solid #20242d;background:rgba(9,11,16,.84);backdrop-filter:blur(16px);position:sticky;top:0;z-index:5}.nav{height:62px;display:flex;align-items:center;justify-content:space-between}.brand{font-weight:900}.brand b{color:#8de8c1}main{padding:34px 0 60px}.layout{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:28px;align-items:start}.preview{background:#10131a;border:1px solid #252b35;border-radius:22px;padding:13px}.preview img{display:block;max-width:100%;max-height:74vh;margin:auto;border-radius:14px;box-shadow:0 25px 70px #0009}.side{position:sticky;top:90px}h1{font-size:clamp(2rem,5vw,3.8rem);line-height:1;letter-spacing:-.055em;margin:0 0 12px}.meta{color:#9ba6b6}.btns{display:grid;gap:10px;margin:20px 0}.btn{display:block;border:0;border-radius:13px;padding:12px 15px;background:#8de8c1;color:#07110d;font-weight:850;text-align:center;text-decoration:none;cursor:pointer}.btn.alt{background:#222936;color:#f4f7fb}.ad{min-height:90px;border:1px dashed #28303c;border-radius:16px;margin:25px 0;overflow:hidden}.note{color:#9ba6b6;font-size:.88rem}.tags{display:flex;flex-wrap:wrap;gap:7px;margin-top:16px}.tag{background:#171c25;border:1px solid #2a313d;border-radius:999px;padding:6px 9px;font-size:.78rem;color:#c3cad5}@media(max-width:820px){.layout{grid-template-columns:1fr}.side{position:static}.preview img{max-height:none}}
</style></head><body>
<nav><div class="w nav"><a href="../" class="brand" style="text-decoration:none">Flux<b>Walls</b></a><a href="../">Latest</a></div></nav>
<main class="w"><div class="layout">
<div class="preview"><img id="art" src="../assets/$asset" width="$width" height="$height" alt="$title"></div>
<aside class="side"><h1>$title</h1><div class="meta">$orientation · $width × $height · $date</div>
<div class="tags">$tags</div><div class="btns">
<a class="btn" href="../assets/$asset" download="$asset">Download SVG</a>
<button class="btn alt" id="pngBtn">Download PNG</button></div>
<p class="note">Original procedural artwork generated automatically. No account required.</p>
<div class="ad"><ins class="adsbygoogle" style="display:block;width:100%" data-ad-client="$ads_client" data-ad-slot="$ads_slot" data-ad-format="auto" data-full-width-responsive="true"></ins><script>try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}</script></div>
</aside></div></main>
<script>
document.getElementById('pngBtn').onclick=async function(){
 const b=this; b.disabled=true; b.textContent='Rendering…';
 try{
  const txt=await (await fetch('../assets/$asset')).text();
  const blob=new Blob([txt],{type:'image/svg+xml'}), u=URL.createObjectURL(blob), im=new Image();
  await new Promise((ok,bad)=>{im.onload=ok;im.onerror=bad;im.src=u});
  const c=document.createElement('canvas'); c.width=$width;c.height=$height;
  c.getContext('2d').drawImage(im,0,0,c.width,c.height); URL.revokeObjectURL(u);
  const out=await new Promise(ok=>c.toBlob(ok,'image/png'));
  const a=document.createElement('a');a.href=URL.createObjectURL(out);a.download='$png_name';a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href),2000);
 }catch(e){alert('PNG rendering failed. SVG download is still available.')}
 b.disabled=false;b.textContent='Download PNG';
};
</script></body></html>""")

INDEX = Template("""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FluxWalls — Free Original Wallpapers Generated Daily</title>
<meta name="description" content="Fresh original abstract wallpapers generated and published automatically every day. Free mobile, desktop and square downloads.">
<meta name="robots" content="index,follow"><link rel="canonical" href="$base"><meta name="theme-color" content="#090b10">
<link rel="alternate" type="application/rss+xml" title="FluxWalls RSS" href="feed.xml">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=$ads_client" crossorigin="anonymous"></script>
<style>
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 20% -10%,#173328 0,transparent 28%),#090b10;color:#f5f7fa;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}.w{width:min(1200px,calc(100% - 28px));margin:auto}nav{position:sticky;top:0;z-index:5;background:rgba(9,11,16,.84);backdrop-filter:blur(16px);border-bottom:1px solid #20242d}.nav{height:62px;display:flex;align-items:center;justify-content:space-between}.brand{font-weight:900}.brand b{color:#8de8c1}.hero{padding:64px 0 30px}.hero h1{font-size:clamp(2.7rem,7vw,5.8rem);line-height:.94;letter-spacing:-.07em;margin:0 0 18px;max-width:900px}.hero p{color:#9ba6b6;font-size:1.1rem;max-width:720px}.pill{display:inline-block;border:1px solid #315145;border-radius:999px;padding:7px 11px;color:#8de8c1;font-size:.82rem;font-weight:800;margin-bottom:18px}.ad{min-height:90px;border:1px dashed #28303c;border-radius:16px;margin:18px 0 34px;overflow:hidden}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.card{display:block;text-decoration:none;color:inherit;background:#10131a;border:1px solid #222934;border-radius:18px;padding:9px;transition:.18s}.card:hover{transform:translateY(-2px);border-color:#3a4657}.thumb{height:280px;border-radius:12px;background:#090b10;display:flex;align-items:center;justify-content:center;overflow:hidden}.thumb img{width:100%;height:100%;object-fit:cover}.info{padding:10px 4px 5px}.title{font-weight:850}.meta{color:#8e99aa;font-size:.78rem;margin-top:3px}footer{margin-top:58px;border-top:1px solid #20242d;padding:26px 0 40px;color:#8e99aa;font-size:.85rem}a{color:inherit}@media(max-width:900px){.grid{grid-template-columns:repeat(3,1fr)}}@media(max-width:650px){.grid{grid-template-columns:repeat(2,1fr)}.thumb{height:245px}} 
</style></head><body><nav><div class="w nav"><div class="brand">Flux<b>Walls</b></div><a href="privacy.html">Privacy</a></div></nav>
<main class="w"><section class="hero"><span class="pill">New batch every day · free</span><h1>Original wallpapers that keep creating themselves.</h1><p>Fresh procedural designs for phones, desktops and square screens. No sign-up and no manual publishing cycle.</p></section>
<div class="ad"><ins class="adsbygoogle" style="display:block;width:100%" data-ad-client="$ads_client" data-ad-slot="$ads_slot" data-ad-format="auto" data-full-width-responsive="true"></ins><script>try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}</script></div>
<section class="grid">$cards</section>
</main><footer><div class="w">FluxWalls · automatically generated original wallpapers · <a href="feed.xml">RSS</a> · <a href="privacy.html">Privacy</a></div></footer></body></html>""")

def title_for(family, orientation, colors, idx):
    names={
      "aurora":"Soft Aurora Flow","halo":"Luminous Halo","waves":"Quiet Gradient Waves",
      "orbital":"Orbital Glow","paper":"Layered Paper Dream","mesh":"Color Mesh Bloom",
      "dusk":"Abstract Dusk Horizon","neon":"Neon Glass Lines"
    }
    suffix=["Nocturne","Drift","Pulse","Veil","Echo","Tide","Bloom","Arc"][idx%8]
    return f"{names[family]} — {suffix}"

def load_catalog():
    p=OUT/"catalog.json"
    if not p.exists(): return []
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return []

def page_for(e):
    tags="".join(f'<span class="tag">{esc(t)}</span>' for t in e["tags"])
    return DETAIL.substitute(
      title=esc(e["title"]),description=esc(e["description"]),canonical=e["url"],
      ads_client=ADS_CLIENT,ads_slot=ADS_SLOT,asset=e["asset"],width=e["width"],height=e["height"],
      orientation=esc(e["orientation"]),date=esc(e["date"]),tags=tags,png_name=e["slug"]+".png"
    )

def main():
    day=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    catalog=load_catalog()
    existing={x["slug"] for x in catalog}
    new=[]
    for i,(orientation,w,h) in enumerate(FORMATS):
        rng=random.Random(seed_for(day,i))
        family=FAMILIES[(rng.randrange(len(FAMILIES))+i)%len(FAMILIES)]
        colors=PALETTES[rng.randrange(len(PALETTES))]
        slug=f"{day}-{family}-{orientation}-{i+1}"
        if slug in existing: continue
        asset=slug+".svg"
        (ASSETS/asset).write_text(make_svg(w,h,family,colors,rng),encoding="utf-8")
        title=title_for(family,orientation,colors,i)
        desc=f"Free {orientation} abstract wallpaper in the {family} style, generated as original procedural artwork on {day}."
        e={
          "slug":slug,"asset":asset,"title":title,"description":desc,"date":day,
          "family":family,"orientation":orientation,"width":w,"height":h,
          "url":BASE+"w/"+slug+".html",
          "tags":[family,orientation,"abstract","wallpaper","procedural","free"]
        }
        (PAGES/(slug+".html")).write_text(page_for(e),encoding="utf-8")
        catalog.append(e); new.append(e)

    catalog=sorted(catalog,key=lambda x:(x["date"],x["slug"]),reverse=True)
    (OUT/"catalog.json").write_text(json.dumps(catalog,ensure_ascii=False,separators=(",",":")),encoding="utf-8")

    cards=[]
    for e in catalog[:96]:
        cards.append(
          f'<a class="card" href="w/{e["slug"]}.html"><div class="thumb"><img loading="lazy" src="assets/{e["asset"]}" alt="{esc(e["title"])}"></div>'
          f'<div class="info"><div class="title">{esc(e["title"])}</div><div class="meta">{esc(e["orientation"])} · {e["width"]}×{e["height"]} · {esc(e["date"])}</div></div></a>'
        )
    (OUT/"index.html").write_text(INDEX.substitute(base=BASE,ads_client=ADS_CLIENT,ads_slot=ADS_SLOT,cards="".join(cards)),encoding="utf-8")

    privacy="""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Privacy — FluxWalls</title><meta name="robots" content="index,follow"><style>body{margin:0;background:#090b10;color:#f5f7fa;font:16px/1.7 system-ui}.w{width:min(760px,calc(100% - 32px));margin:60px auto}a{color:#8de8c1}p{color:#aab3c0}</style></head><body><main class="w"><p><a href="./">← FluxWalls</a></p><h1>Privacy</h1><p>FluxWalls requires no account and runs as a static website on GitHub Pages.</p><p>Wallpaper PNG conversion happens locally in the browser. The site does not operate its own user database.</p><p>Google AdSense may serve advertising and can use cookies or similar technologies according to Google's policies and applicable consent requirements.</p></main></body></html>"""
    (OUT/"privacy.html").write_text(privacy,encoding="utf-8")

    urls=[BASE,BASE+"privacy.html"]+[e["url"] for e in catalog[:1000]]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc></url>\n' for u in urls)+'</urlset>\n'
    (OUT/"sitemap.xml").write_text(sm,encoding="utf-8")
    (OUT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+BASE+"sitemap.xml\n",encoding="utf-8")

    rss_items=[]
    for e in catalog[:30]:
        rss_items.append(f'<item><title>{esc(e["title"])}</title><link>{e["url"]}</link><guid>{e["url"]}</guid><description>{esc(e["description"])}</description></item>')
    rss='<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>FluxWalls</title><link>'+BASE+'</link><description>Fresh original wallpapers generated daily.</description>'+''.join(rss_items)+'</channel></rss>'
    (OUT/"feed.xml").write_text(rss,encoding="utf-8")

    (OUT/(INDEXNOW_KEY+".txt")).write_text(INDEXNOW_KEY,encoding="utf-8")
    idx={
      "host":"thobg01.github.io",
      "key":INDEXNOW_KEY,
      "keyLocation":BASE+INDEXNOW_KEY+".txt",
      "urlList":[BASE]+[e["url"] for e in new]
    }
    (OUT/"indexnow.json").write_text(json.dumps(idx,separators=(",",":")),encoding="utf-8")
    print("FluxWalls generated",len(new),"new wallpapers for",day)

if __name__=="__main__":
    main()
