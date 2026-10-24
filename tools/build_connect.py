from common import *

p = 'c'
W, H = 1000, 540
body = card(p, 0, 0, W, H, 30)

body += f'''<ellipse cx="190" cy="300" rx="190" ry="250" fill="url(#{p}-gv)"/>
<ellipse cx="300" cy="140" rx="160" ry="110" fill="url(#{p}-gc)"/>
<g class="rise" style="animation-delay:.1s"><g>
<animateTransform attributeName="transform" type="translate" values="0 0;0 -7;0 0" dur="4s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".4 0 .6 1;.4 0 .6 1"/>
<image x="14" y="10" width="346" height="520" xlink:href="data:image/png;base64,{b64file(ASSETS / 'point.png')}"/></g></g>'''

body += f'''<g class="rise" style="animation-delay:.3s"><text x="410" y="62" class="m" font-size="11" letter-spacing="2.4" fill="{CYAN}">// CONNECT</text>
<text x="410" y="100" class="d" font-weight="700" font-size="34" fill="#f1f5f9">Let's build something</text>
<text x="410" y="128" class="d" font-weight="700" font-size="34" fill="url(#{p}-tx)">worth shipping.</text></g>
<defs><linearGradient id="{p}-tx" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".6" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient></defs>'''

chat = '<path d="M4 5h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1h-9l-5 4v-4H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1z" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/><path d="M8 10h8M8 13h5" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>'
cards = [
    ('GitHub', D['github_url'].replace('https://', ''), CYAN, f'<path d="{icon_path("github")}" fill="{CYAN}"/>'),
    ('Email', D['email'], VIOLET, f'<path d="{icon_path("gmail")}" fill="{VIOLET}"/>'),
    ('Start a collab', 'Pitch an idea in a GitHub issue', PINK, chat.format(c=PINK)),
]
CXL, CW_, CH_ = 410, 550, 92
for i, (t, s, col, ic) in enumerate(cards):
    y = 160 + i * (CH_ + 18)
    body += f'''<g class="slide" style="animation-delay:{.5 + i * .15}s">
<rect x="{CXL}" y="{y}" width="{CW_}" height="{CH_}" rx="22" fill="#ffffff08"/>
<rect x="{CXL + .6}" y="{y + .6}" width="{CW_ - 1.2}" height="{CH_ - 1.2}" rx="21.4" fill="none" stroke="{col}" stroke-opacity=".45"/>
<rect x="{CXL + 20}" y="{y + 18}" width="56" height="56" rx="16" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>
<g transform="translate({CXL + 34},{y + 32}) scale(1.17)">{ic}</g>
<text x="{CXL + 98}" y="{y + 40}" class="d" font-weight="700" font-size="22" fill="#f1f5f9">{t}</text>
<text x="{CXL + 98}" y="{y + 64}" class="m" font-size="12.5" fill="#94a3b8">{s}</text>
<g class="nudge" style="animation-delay:{i * .25}s"><path d="M{CXL + CW_ - 64} {y + 46}h26m-9 -9l9 9l-9 9" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g></g>'''

body += f'<g class="rise" style="animation-delay:1.2s"><text x="{CXL}" y="{H - 28}" class="m" font-size="11.5" fill="#64748b">Based in {D["city"]} · Full Stack at {D["company"]} · always up for a good collab</text></g>'

open(ASSETS / 'connect.svg', 'w').write(wrap(p, W, H, body, 'Connect: GitHub, email and collaboration links with a pointing character'))
print('connect.svg KB', (ASSETS / 'connect.svg').stat().st_size // 1024)
