import random
from common import *

p = 'i'
W, H = 1000, 580
LW = 360
DX = 380
LOOP = 14.0
body = card(p, 0, 0, LW, H, 30) + card(p, DX, 0, W - DX, H, 30)

defs = f'''<linearGradient id="{p}-strap" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="{p}-metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1f5f9"/><stop offset=".5" stop-color="#94a3b8"/><stop offset="1" stop-color="#475569"/></linearGradient>
<linearGradient id="{p}-gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fde68a"/><stop offset=".5" stop-color="#f59e0b"/><stop offset="1" stop-color="#b45309"/></linearGradient>
<linearGradient id="{p}-foil" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".3" stop-color="{CYAN}" stop-opacity=".45"/><stop offset=".5" stop-color="{PINK}" stop-opacity=".5"/><stop offset=".7" stop-color="{VIOLET}" stop-opacity=".45"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>
<linearGradient id="{p}-bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#171829"/><stop offset="1" stop-color="#0f1020"/></linearGradient>
<clipPath id="{p}-lw"><rect x="0" y="0" width="{LW}" height="{H}" rx="30"/></clipPath>
<clipPath id="{p}-bc"><rect x="60" y="170" width="240" height="378" rx="22"/></clipPath>
<clipPath id="{p}-pc"><rect x="100" y="218" width="160" height="160" rx="22"/></clipPath>
<linearGradient id="{p}-nm" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'''

# ---------------------------------------------------------------- pendulum samples
DT = .05
n = int(LOOP / DT)
swing, drop = [], []
T_DROP = .7
for k in range(n + 1):
    t = k * DT
    if t < T_DROP:
        drop.append(f'0 {fmt(-440 * (1 - (t / T_DROP) ** 2))}')
        swing.append('0 180 0')
    else:
        s = t - T_DROP
        ang = 15 * math.exp(-s / 1.9) * math.cos(2 * math.pi * s / 2.3)
        drop.append('0 0')
        swing.append(f'{fmt(ang)} 180 0')

# bars of the barcode
rng = random.Random(11)
bars, x = '', 128
while x < 276:
    w_ = rng.choice([1.5, 1.5, 2.5, 3.5])
    bars += f'<rect x="{x}" y="486" width="{w_}" height="34" fill="#e2e8f0"/>'
    x += w_ + rng.choice([1.5, 2, 3])

name_defs = ''
badge = f'''<g clip-path="url(#{p}-lw)"><g><animateTransform attributeName="transform" type="translate" values="{';'.join(drop)}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>
<g><animateTransform attributeName="transform" type="rotate" values="{';'.join(swing)}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>
<!-- strap -->
<rect x="162" y="-60" width="36" height="196" fill="url(#{p}-strap)"/>
<rect x="162" y="-60" width="3" height="196" fill="#fff" fill-opacity=".25"/><rect x="195" y="-60" width="3" height="196" fill="#000" fill-opacity=".25"/>
<g class="m" font-size="9" font-weight="700" fill="{BG}" fill-opacity=".72" letter-spacing="2.2">
<text transform="translate(184,-52) rotate(90)">SHAHRIAR KALAM EMON · {D['company'].upper()} · FULL STACK ·</text></g>
<!-- clasp -->
<rect x="170" y="124" width="20" height="22" rx="4" fill="url(#{p}-metal)"/>
<rect x="164" y="140" width="32" height="20" rx="6" fill="url(#{p}-metal)" stroke="#1e293b"/>
<ellipse cx="180" cy="166" rx="9" ry="10" fill="none" stroke="url(#{p}-metal)" stroke-width="4"/>
<!-- badge -->
<rect x="60" y="170" width="240" height="378" rx="22" fill="url(#{p}-bd)"/>
<g clip-path="url(#{p}-bc)"><rect x="60" y="170" width="240" height="378" fill="url(#{p}-dots)"/>
<ellipse cx="180" cy="300" rx="130" ry="140" fill="url(#{p}-gv)"/><ellipse cx="260" cy="520" rx="130" ry="80" fill="url(#{p}-gp)"/>
<rect x="60" y="170" width="240" height="40" fill="#ffffff08"/></g>
<rect x="152" y="180" width="56" height="9" rx="4.5" fill="#05060a" stroke="#ffffff22"/>
<text x="80" y="204" class="m" font-size="10" font-weight="700" letter-spacing="2.5" fill="#e2e8f0">{D['company'].upper()}</text>
<text x="280" y="204" class="m" font-size="9" letter-spacing="1.5" fill="{CYAN}" text-anchor="end">DEV</text>
<!-- portrait -->
<rect x="96" y="214" width="168" height="168" rx="26" fill="#0a0b12" stroke="#ffffff1a"/>
<image x="100" y="218" width="160" height="160" clip-path="url(#{p}-pc)" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/png;base64,{b64file(ASSETS / 'portrait.png')}"/>
<rect x="98" y="216" width="164" height="164" rx="24" fill="none" stroke="url(#{p}-hair)" stroke-width="2" stroke-opacity=".5" pathLength="100"/>
<rect x="98" y="216" width="164" height="164" rx="24" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" pathLength="100" stroke-dasharray="9 91" stroke-dashoffset="0">
<animate attributeName="stroke-dashoffset" values="0;-100" dur="3.2s" repeatCount="indefinite"/></rect>
<rect x="98" y="216" width="164" height="164" rx="24" fill="none" stroke="{CYAN}" stroke-width="6" stroke-linecap="round" pathLength="100" stroke-dasharray="9 91" stroke-dashoffset="0" opacity=".45" style="filter:blur(3px)">
<animate attributeName="stroke-dashoffset" values="0;-100" dur="3.2s" repeatCount="indefinite"/></rect>
<!-- name -->
<text x="180" y="414" class="d" font-weight="700" font-size="24" fill="#f1f5f9" text-anchor="middle" letter-spacing="1">{D['name1']}</text>
<text x="180" y="438" class="d" font-weight="700" font-size="24" fill="url(#{p}-nm)" text-anchor="middle" letter-spacing="1">{D['name2']}</text>
<text x="180" y="458" class="m" font-size="9" letter-spacing="1.8" fill="{CYAN}" text-anchor="middle">FULL STACK WEB DEVELOPER</text>
<!-- chip + barcode -->
<rect x="80" y="482" width="38" height="30" rx="6" fill="url(#{p}-gold)"/>
<path d="M80 497h38M92 482v30M106 482v30M92 490h14M92 504h14" stroke="#7c4a03" stroke-width="1.1" fill="none" stroke-opacity=".8"/>
{bars}
<text x="180" y="538" class="m" font-size="8.5" letter-spacing="2" fill="#94a3b8" text-anchor="middle">{D['city'].upper()} · {D['company'].upper()}</text>
<!-- foil sweep -->
<g clip-path="url(#{p}-bc)"><rect x="-160" y="150" width="110" height="420" fill="url(#{p}-foil)" transform="skewX(-18)" style="mix-blend-mode:screen">
<animate attributeName="x" values="-160;-160;420;420" keyTimes="0;.5;.78;1" dur="{LOOP / 2}s" begin="0s" repeatCount="indefinite"/></rect></g>
<rect x="60.6" y="170.6" width="238.8" height="376.8" rx="21.4" fill="none" stroke="url(#{p}-hair)" stroke-width="1.4"/>
</g></g></g>'''
body += badge

# ---------------------------------------------------------------- dashboard
PAD = 28
x0 = DX + PAD
body += f'''<g class="rise" style="animation-delay:.2s"><text x="{x0}" y="42" class="m" font-size="11" letter-spacing="2.4" fill="{CYAN}">// DASHBOARD</text>
<circle cx="{W - PAD - 54}" cy="38" r="4" fill="#34d399"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="{W - PAD}" y="42" class="m" font-size="11" letter-spacing="2" fill="#94a3b8" text-anchor="end">LIVE</text></g>'''

kpis = [('REPOS', D['repos'], 'public', CYAN), ('STARS', D['stars'], 'earned', VIOLET), ('COMMITS', D['commits'], 'this year', PINK)]
tw, tg = 178, 14
steps = 14
t0c, dtc = 1.1, .1
for i, (lab, val, sub, col) in enumerate(kpis):
    tx = x0 + i * (tw + tg)
    body += f'''<g class="rise" style="animation-delay:{.3 + i * .12}s"><rect x="{tx}" y="64" width="{tw}" height="96" rx="18" fill="#ffffff08" stroke="{col}" stroke-opacity=".35"/>
<rect x="{tx + 16}" y="80" width="18" height="3" rx="1.5" fill="{col}"/>
<text x="{tx + 16}" y="104" class="m" font-size="10.5" letter-spacing="2" fill="#94a3b8">{lab}</text>
<text x="{tx + tw - 16}" y="104" class="m" font-size="10" fill="{col}" text-anchor="end">{sub}</text></g>'''
    for k in range(steps + 1):
        v = round(val * ease_out(k / steps))
        a = (t0c + dtc * k) / LOOP
        b_ = (t0c + dtc * (k + 1)) / LOOP
        if k == 0:
            vs, ks = 'visible;hidden', [0, b_]
        elif k == steps:
            vs, ks = 'hidden;visible', [0, a]
        else:
            vs, ks = 'hidden;visible;hidden', [0, a, b_]
        vis = 'visible' if k == steps else 'hidden'
        body += (f'<text x="{tx + 16}" y="146" class="d" font-weight="700" font-size="40" fill="#f1f5f9" visibility="{vis}">{v:,}'
                 f'<animate attributeName="visibility" values="{vs}" keyTimes="{";".join(fmt(x) for x in ks)}" calcMode="discrete" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/></text>')

# bar chart
cy0 = 190
body += f'<g class="rise" style="animation-delay:.6s"><text x="{x0}" y="{cy0 + 6}" class="d" font-weight="700" font-size="17" fill="#f1f5f9">Most starred repos</text>' \
        f'<text x="{W - PAD}" y="{cy0 + 6}" class="m" font-size="10.5" fill="#94a3b8" text-anchor="end">stars</text></g>'
mx = max(v for _, v in D['top_repos'])
bx0, bwid = x0 + 150, 330
for r, (nm, v) in enumerate(D['top_repos']):
    y = cy0 + 28 + r * 34
    w_ = bwid * v / mx
    a = .04 + r * .035
    kt = [0, a, a + .22, 1]
    body += f'''<g class="rise" style="animation-delay:{.7 + r * .08}s"><text x="{x0}" y="{y + 15}" class="m" font-size="12" fill="#cbd5e1">{nm}</text>
<rect x="{bx0}" y="{y + 3}" width="{bwid}" height="16" rx="8" fill="#ffffff0c"/>
<rect x="{bx0}" y="{y + 3}" width="{fmt(w_)}" height="16" rx="8" fill="{VIOLET}">
<animate attributeName="width" values="0;0;{fmt(w_)};{fmt(w_)}" keyTimes="{";".join(fmt(k) for k in [0, a, a + .22, 1])}" dur="{LOOP / 1.75}s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;.2 .8 .2 1;0 0 1 1"/></rect>
<text x="{W - PAD}" y="{y + 15.5}" class="m" font-size="12.5" font-weight="700" fill="#f1f5f9" text-anchor="end">{v}</text></g>'''

# now panel
ny = 410
body += f'''<g class="rise" style="animation-delay:1.1s"><rect x="{x0}" y="{ny}" width="{W - DX - 2 * PAD}" height="138" rx="20" fill="#ffffff08" stroke="url(#{p}-hair)" stroke-opacity=".5"/>
<circle cx="{x0 + 22}" cy="{ny + 26}" r="4" fill="{PINK}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>
<text x="{x0 + 36}" y="{ny + 30}" class="m" font-size="11" font-weight="700" letter-spacing="2.4" fill="#e2e8f0">NOW</text>'''
now = [('Building', f"full stack products at {D['company']}", CYAN), ('Learning', 'new languages and cultures', VIOLET), ('Open to', 'collabs and fresh ideas', PINK)]
for j, (k_, v_, col) in enumerate(now):
    yy = ny + 62 + j * 28
    body += (f'<text x="{x0 + 22}" y="{yy}" class="m" font-size="12.5" font-weight="700" fill="{col}">{k_}</text>'
             f'<text x="{x0 + 108}" y="{yy}" class="m" font-size="12.5" fill="#cbd5e1">{v_}</text>')
body += f'<rect x="{x0 + 108 + 8.0 * len("collabs and fresh ideas") + 4}" y="{ny + 62 + 56 - 12}" width="7" height="14" fill="{CYAN}"><animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" dur="1s" repeatCount="indefinite" calcMode="discrete"/></rect></g>'

open(ASSETS / 'id-dashboard.svg', 'w').write(wrap(p, W, H, body, 'ID badge on a swinging lanyard beside a stats dashboard', defs))
print('id-dashboard.svg KB', (ASSETS / 'id-dashboard.svg').stat().st_size // 1024)
