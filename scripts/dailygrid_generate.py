from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import random, json, html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "dailygrid"
ARCHIVE = OUT / "archive"
OUT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

ADS_CLIENT = "ca-pub-9886017981009232"
ADS_SLOT = "4586711336"
BASE = "https://thobg01.github.io/Wallpapers/dailygrid/"

WORDS = [
    ("lantern","portable light"),("citadel","fortified stronghold"),("nebula","cloud in space"),
    ("harvest","gathered crop"),("cascade","falling sequence"),("quartz","common crystal"),
    ("voyage","long journey"),("ember","glowing coal"),("meadow","grassy field"),
    ("cipher","coded message"),("orbit","path around a body"),("velvet","soft fabric"),
    ("summit","highest point"),("anchor","keeps a vessel in place"),("comet","icy body with a tail"),
    ("riddle","puzzle in words"),("forge","workshop for metal"),("signal","transmitted sign"),
    ("breeze","gentle wind"),("mosaic","image made from pieces")
]

def date_seed(day: str) -> int:
    return int(day.replace("-","")) * 7919 + 104729

def sudoku(rng):
    base, side = 3, 9
    pattern = lambda r,c: (base*(r%base)+r//base+c)%side
    def sh(seq):
        x=list(seq); rng.shuffle(x); return x
    rb=range(base)
    rows=[g*base+r for g in sh(rb) for r in sh(rb)]
    cols=[g*base+c for g in sh(rb) for c in sh(rb)]
    nums=sh(range(1,10))
    board=[[nums[pattern(r,c)] for c in cols] for r in rows]
    solution=[r[:] for r in board]
    cells=list(range(81)); rng.shuffle(cells)
    for i in cells[:48]:
        board[i//9][i%9]=0
    return board, solution

def lights_out(rng):
    n=5
    b=[[0]*n for _ in range(n)]
    def toggle(r,c):
        for dr,dc in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
            rr,cc=r+dr,c+dc
            if 0<=rr<n and 0<=cc<n:
                b[rr][cc]^=1
    for r in range(n):
        for c in range(n):
            if rng.random()<0.34:
                toggle(r,c)
    if not any(map(any,b)):
        toggle(2,2)
    return b

def math_target(rng):
    nums=[rng.randint(2,14) for _ in range(5)]
    a,b=rng.sample(nums,2)
    return nums, (a+b if rng.random()<0.5 else a*b)

def sequence(rng):
    if rng.random()<0.5:
        start,step=rng.randint(3,30),rng.randint(2,11)
        vals=[start+i*step for i in range(6)]
        rule=f"Add {step} each time."
    else:
        start,a,b=rng.randint(1,12),rng.randint(2,5),rng.randint(3,7)
        vals=[start]
        for i in range(5):
            vals.append(vals[-1]+(a if i%2==0 else b))
        rule=f"Alternate +{a}, +{b}."
    idx=rng.randint(1,4)
    ans=vals[idx]; shown=vals[:]; shown[idx]="?"
    return shown,ans,rule

def scramble(rng):
    word,hint=rng.choice(WORDS)
    chars=list(word)
    for _ in range(10):
        rng.shuffle(chars)
        if "".join(chars)!=word:
            break
    return "".join(chars),word,hint

def build(day, board, solution, lights, nums, target, seq, seqans, seqrule, scr, word, hint, archive=False):
    pretty=datetime.strptime(day,"%Y-%m-%d").strftime("%B %d, %Y")
    canonical=BASE+(f"archive/{day}.html" if archive else "")
    nav='<a href="../">← Today</a>' if archive else '<a href="#games">Play</a><a href="archive/">Archive</a><a href="privacy.html">Privacy</a>'
    chips="".join(f'<span class="chip">{n}</span>' for n in nums)
    seqtext=" · ".join(map(str,seq))
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DailyGrid — Free Daily Puzzles for {html.escape(pretty)}</title>
<meta name="description" content="Play five free daily puzzles: Sudoku, Lights Out, target math, number sequence and word scramble. No account required.">
<meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><meta name="theme-color" content="#090d16">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS_CLIENT}" crossorigin="anonymous"></script>
<style>
:root{{--bg:#090d16;--panel:#101727;--line:#24314d;--text:#f5f7ff;--muted:#9eabc0;--a:#78f0bd}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;background:radial-gradient(circle at 15% -10%,#183b35 0,transparent 27%),radial-gradient(circle at 90% 0,#19284b 0,transparent 27%),var(--bg);color:var(--text);line-height:1.5}}a{{color:inherit}}.w{{width:min(1100px,calc(100% - 28px));margin:auto}}nav{{position:sticky;top:0;z-index:9;background:rgba(9,13,22,.82);backdrop-filter:blur(18px);border-bottom:1px solid rgba(255,255,255,.06)}}.nav{{height:64px;display:flex;align-items:center;justify-content:space-between}}.brand{{font-weight:900;letter-spacing:-.04em}}.brand span{{color:var(--a)}}.links{{display:flex;gap:16px;color:var(--muted);font-size:.9rem}}.links a{{text-decoration:none}}.hero{{padding:58px 0 28px}}.tag{{display:inline-block;padding:7px 11px;border:1px solid #315648;border-radius:999px;color:var(--a);font-size:.8rem;font-weight:800}}h1{{font-size:clamp(2.5rem,7vw,5.2rem);line-height:.96;letter-spacing:-.065em;margin:18px 0 14px;max-width:850px}}.hero p{{color:var(--muted);font-size:1.08rem;max-width:710px}}.ad{{min-height:88px;margin:24px 0 34px;display:flex;align-items:center;border:1px dashed #2a3550;border-radius:18px;overflow:hidden}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}.card{{background:linear-gradient(180deg,var(--panel),#0c1220);border:1px solid var(--line);border-radius:22px;padding:20px;box-shadow:0 18px 50px rgba(0,0,0,.25)}}.card h2{{margin:0 0 4px;letter-spacing:-.03em}}.card p{{margin:0 0 15px;color:var(--muted);font-size:.9rem}}button,input{{font:inherit}}button{{border:0;border-radius:11px;background:var(--a);color:#06110d;padding:10px 13px;font-weight:850;cursor:pointer}}button.alt{{background:#25314a;color:#eef3ff}}.status{{min-height:43px;margin-top:12px;padding:10px 12px;border-radius:11px;border:1px solid #26324b;background:#0b101c;color:#ccd5e5}}.sudoku{{display:grid;grid-template-columns:repeat(9,1fr);max-width:450px;aspect-ratio:1;margin:auto;border:2px solid #7e8da6}}.cell{{width:100%;min-width:0;text-align:center;background:#0b101c;color:#fff;border:1px solid #26324b;border-radius:0;padding:0;font-weight:700}}.cell:nth-child(3n){{border-right-color:#7e8da6}}.cell:nth-child(9n){{border-right:0}}.fixed{{background:#18233a;color:#b8c6db}}.lights{{display:grid;grid-template-columns:repeat(5,1fr);gap:7px;max-width:360px;margin:auto}}.light{{aspect-ratio:1;background:#141c2e;border:1px solid #2d3b5b;padding:0}}.light.on{{background:#78f0bd;box-shadow:0 0 22px rgba(120,240,189,.28)}}.big{{font-size:clamp(1.7rem,5vw,2.6rem);font-weight:900;letter-spacing:.04em;margin:8px 0 15px}}.chips{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}}.chip{{padding:8px 11px;background:#18233a;border:1px solid #2a3858;border-radius:10px;font-weight:800}}input[type=text],input[type=number]{{width:100%;background:#0b101c;border:1px solid #31405f;color:#fff;padding:11px 12px;border-radius:11px;margin-bottom:10px}}footer{{margin-top:56px;border-top:1px solid var(--line);padding:28px 0 40px;color:var(--muted);font-size:.88rem}}@media(max-width:760px){{.grid{{grid-template-columns:1fr}}.links{{font-size:.8rem}}.card{{padding:16px}}}}
</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"DailyGrid","applicationCategory":"GameApplication","operatingSystem":"Any","offers":{{"@type":"Offer","price":"0","priceCurrency":"EUR"}}}}</script>
</head><body><nav><div class="w nav"><div class="brand">Daily<span>Grid</span></div><div class="links">{nav}</div></div></nav>
<main class="w"><section class="hero"><span class="tag">New puzzles every day · free</span><h1>Five quick puzzles. One fresh grid every day.</h1><p>{pretty}. No account, no leaderboard, no pressure. Everything runs in your browser.</p></section>
<div class="ad"><ins class="adsbygoogle" style="display:block;width:100%" data-ad-client="{ADS_CLIENT}" data-ad-slot="{ADS_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>try{{(adsbygoogle=window.adsbygoogle||[]).push({{}})}}catch(e){{}}</script></div>
<section id="games" class="grid">
<article class="card"><h2>Daily Sudoku</h2><p>Fill every row, column and 3×3 box with 1–9.</p><div id="sudoku" class="sudoku"></div><div style="display:flex;gap:8px;margin-top:12px"><button id="checkSudoku">Check</button><button class="alt" id="resetSudoku">Reset</button></div><div class="status" id="sudokuStatus">Medium puzzle · 33 clues.</div></article>
<article class="card"><h2>Lights Out</h2><p>Turn every tile dark. Tapping a tile flips it and its neighbors.</p><div id="lights" class="lights"></div><div style="display:flex;gap:8px;margin-top:12px"><button class="alt" id="resetLights">Reset</button></div><div class="status" id="lightsStatus">Solve today's 5×5 board.</div></article>
<article class="card"><h2>Target Math</h2><p>Use any of these numbers to reach the target.</p><div class="chips">{chips}</div><div class="big">Target: {target}</div><input id="mathAnswer" type="text" placeholder="Type an expression, e.g. 8 × 7"><button id="mathCheck">Check value</button><div class="status" id="mathStatus">Use +, −, × or ÷. You do not have to use every number.</div></article>
<article class="card"><h2>Missing Number</h2><p>Find the value that completes today's sequence.</p><div class="big">{seqtext}</div><input id="seqAnswer" type="number" placeholder="Missing number"><button id="seqCheck">Check</button><div class="status" id="seqStatus">Look for a simple repeating pattern.</div></article>
<article class="card"><h2>Word Scramble</h2><p>Unscramble the letters. Hint: {html.escape(hint)}.</p><div class="big">{html.escape(scr.upper())}</div><input id="wordAnswer" type="text" autocomplete="off" placeholder="Your answer"><button id="wordCheck">Check</button><div class="status" id="wordStatus">One English word.</div></article>
<article class="card"><h2>Daily streak</h2><p>Your streak is stored only on this device.</p><div class="big"><span id="streak">0</span> days</div><div class="status">Complete at least three puzzles today to extend it. No account required.</div></article>
</section>
<div class="ad"><ins class="adsbygoogle" style="display:block;width:100%" data-ad-client="{ADS_CLIENT}" data-ad-slot="{ADS_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>try{{(adsbygoogle=window.adsbygoogle||[]).push({{}})}}catch(e){{}}</script></div>
</main><footer><div class="w">DailyGrid · automatically generated daily puzzles · <a href="{('../privacy.html' if archive else 'privacy.html')}">Privacy</a></div></footer>
<script>
const DAY={json.dumps(day)},SUDOKU={json.dumps(board,separators=(',',':'))},SOL={json.dumps(solution,separators=(',',':'))},LIGHTS0={json.dumps(lights,separators=(',',':'))},SEQANS={seqans},SEQRULE={json.dumps(seqrule)},WORD={json.dumps(word.lower())},TARGET={target};let completed=new Set();
function done(k){{completed.add(k);if(completed.size>=3)updateStreak()}}
function updateStreak(){{let s=JSON.parse(localStorage.getItem('dailygridStreak')||'{{"last":"","count":0}}');if(s.last===DAY){{document.getElementById('streak').textContent=s.count;return}}let prev=new Date(DAY+'T00:00:00Z');prev.setUTCDate(prev.getUTCDate()-1);let pd=prev.toISOString().slice(0,10);s.count=s.last===pd?s.count+1:1;s.last=DAY;localStorage.setItem('dailygridStreak',JSON.stringify(s));document.getElementById('streak').textContent=s.count}}
(function(){{const el=document.getElementById('sudoku');function draw(){{el.innerHTML='';SUDOKU.flat().forEach((v,i)=>{{let x=document.createElement('input');x.maxLength=1;x.inputMode='numeric';x.className='cell'+(v?' fixed':'');x.value=v||'';x.dataset.i=i;if(v)x.readOnly=true;el.appendChild(x)}})}}draw();document.getElementById('resetSudoku').onclick=draw;document.getElementById('checkSudoku').onclick=()=>{{let ok=true,full=true;[...el.children].forEach((x,i)=>{{if(!x.value)full=false;if(Number(x.value)!==SOL[Math.floor(i/9)][i%9])ok=false}});document.getElementById('sudokuStatus').textContent=ok&&full?'Solved!':full?'Not quite — check the grid.':'Fill every empty cell first.';if(ok&&full)done('sudoku')}}}})();
(function(){{let b=LIGHTS0.map(r=>r.slice()),el=document.getElementById('lights');function toggle(r,c){{[[0,0],[1,0],[-1,0],[0,1],[0,-1]].forEach(([dr,dc])=>{{let rr=r+dr,cc=c+dc;if(rr>=0&&rr<5&&cc>=0&&cc<5)b[rr][cc]^=1}});draw()}}function draw(){{el.innerHTML='';for(let r=0;r<5;r++)for(let c=0;c<5;c++){{let q=document.createElement('button');q.className='light'+(b[r][c]?' on':'');q.onclick=()=>toggle(r,c);el.appendChild(q)}}if(!b.flat().some(Boolean)){{document.getElementById('lightsStatus').textContent='Solved!';done('lights')}}}}draw();document.getElementById('resetLights').onclick=()=>{{b=LIGHTS0.map(r=>r.slice());document.getElementById('lightsStatus').textContent="Solve today's 5×5 board.";draw()}}}})();
document.getElementById('seqCheck').onclick=()=>{{let ok=Number(document.getElementById('seqAnswer').value)===SEQANS;document.getElementById('seqStatus').textContent=ok?'Correct — '+SEQRULE:'Not yet. Try the differences between terms.';if(ok)done('seq')}};
document.getElementById('wordCheck').onclick=()=>{{let ok=document.getElementById('wordAnswer').value.trim().toLowerCase()===WORD;document.getElementById('wordStatus').textContent=ok?'Correct!':'Not yet — use the hint and every letter.';if(ok)done('word')}};
document.getElementById('mathCheck').onclick=()=>{{let raw=document.getElementById('mathAnswer').value.replace(/×/g,'*').replace(/÷/g,'/').replace(/−/g,'-');if(!/^[0-9+\\-*/().\\s]+$/.test(raw))return document.getElementById('mathStatus').textContent='Use numbers and arithmetic operators only.';try{{let v=Function('"use strict";return ('+raw+')')();let ok=Math.abs(v-TARGET)<1e-9;document.getElementById('mathStatus').textContent=ok?'Correct!':'That equals '+v+', not '+TARGET+'.';if(ok)done('math')}}catch(e){{document.getElementById('mathStatus').textContent='That expression could not be calculated.'}}}};
let st=JSON.parse(localStorage.getItem('dailygridStreak')||'{{"last":"","count":0}}');document.getElementById('streak').textContent=st.count||0;
</script></body></html>"""

def archive_index(dates):
    links="".join(f'<li><a href="{d}.html">{d}</a></li>' for d in sorted(dates,reverse=True)[:180])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DailyGrid Puzzle Archive</title><meta name="description" content="Play previous DailyGrid daily puzzle sets."><meta name="robots" content="index,follow"><style>body{{margin:0;background:#090d16;color:#f5f7ff;font:16px/1.6 system-ui}}main{{width:min(760px,calc(100% - 32px));margin:60px auto}}a{{color:#78f0bd}}li{{margin:9px 0}}</style></head><body><main><p><a href="../">← Today's puzzles</a></p><h1>DailyGrid archive</h1><p>Previous automatically generated daily puzzle sets.</p><ul>{links}</ul></main></body></html>"""

def privacy():
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Privacy — DailyGrid</title><meta name="robots" content="index,follow"><style>body{margin:0;background:#090d16;color:#f5f7ff;font:16px/1.7 system-ui}main{width:min(760px,calc(100% - 32px));margin:60px auto}a{color:#78f0bd}p{color:#b4bfd1}</style></head><body><main><p><a href="./">← DailyGrid</a></p><h1>Privacy</h1><p>DailyGrid does not require an account. Puzzle progress and streak data are stored locally in your browser.</p><p>The site is served through GitHub Pages. Advertising may be provided by Google AdSense, which can use cookies or similar technologies according to Google's policies and applicable consent requirements.</p><p>DailyGrid has no custom user database and does not intentionally upload puzzle answers or local progress to an application server.</p></main></body></html>"""

def main():
    day=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rng=random.Random(date_seed(day))
    board,sol=sudoku(rng); lights=lights_out(rng); nums,target=math_target(rng)
    seq,seqans,seqrule=sequence(rng); scr,word,hint=scramble(rng)
    (OUT/"index.html").write_text(build(day,board,sol,lights,nums,target,seq,seqans,seqrule,scr,word,hint),encoding="utf-8")
    (ARCHIVE/f"{day}.html").write_text(build(day,board,sol,lights,nums,target,seq,seqans,seqrule,scr,word,hint,True),encoding="utf-8")
    dates=[p.stem for p in ARCHIVE.glob("????-??-??.html")]
    (ARCHIVE/"index.html").write_text(archive_index(dates),encoding="utf-8")
    (OUT/"privacy.html").write_text(privacy(),encoding="utf-8")
    urls=[BASE,BASE+"archive/",BASE+"privacy.html"]+[BASE+"archive/"+d+".html" for d in sorted(dates,reverse=True)[:180]]
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f"<url><loc>{u}</loc></url>\n" for u in urls)+"</urlset>\n"
    (OUT/"sitemap.xml").write_text(sitemap,encoding="utf-8")
    (OUT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+BASE+"sitemap.xml\n",encoding="utf-8")
    print("DailyGrid generated:",day)

if __name__=="__main__":
    main()
