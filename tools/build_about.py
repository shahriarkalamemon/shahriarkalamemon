from common import *

p = 'a'
W, H = 1000, 520
body = card(p, 0, 0, 488, H, 28) + card(p, 512, 0, 488, H, 28)


def stroke_icon(inner, color):
    return f'<g fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{inner}</g>'


ICON = {
    'layout': '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M9 9v11"/>',
    'server': '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01"/>',
    'rocket': '<path d="M5 15c-1.5 1-2 4-2 5 1 0 4-.5 5-2"/><path d="M12 15l-3-3a22 22 0 0 1 2-4 12 12 0 0 1 9-5c0 3-1.5 7-5 9-1.3.9-3 1.7-3 3z"/><circle cx="15" cy="9" r="1"/>',
}

# ================================================================ LEFT: browser window
bx, by, bw, bh = 24, 24, 440, 262
body += f'''<defs>
<clipPath id="{p}-win"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16"/></clipPath>
<linearGradient id="{p}-page" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#151628"/><stop offset="1" stop-color="#1b1330"/></linearGradient>
<linearGradient id="{p}-tx" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/></linearGradient></defs>
<g class="pop" style="animation-delay:.1s">
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16" fill="#0a0b12"/>
<g clip-path="url(#{p}-win)">
<rect x="{bx}" y="{by}" width="{bw}" height="38" fill="#12131f"/>
<rect x="{bx}" y="{by + 38}" width="{bw}" height="{bh - 38}" fill="url(#{p}-page)"/>
<circle cx="{bx + 20}" cy="{by + 19}" r="5.5" fill="#f87171"/><circle cx="{bx + 38}" cy="{by + 19}" r="5.5" fill="#fbbf24"/><circle cx="{bx + 56}" cy="{by + 19}" r="5.5" fill="#34d399"/>
<rect x="{bx + 82}" y="{by + 7}" width="{bw - 104}" height="24" rx="12" fill="#ffffff0d" stroke="#ffffff18"/>
<path d="M{bx + 98} {by + 16}v-2a4 4 0 0 1 8 0v2" fill="none" stroke="{CYAN}" stroke-width="1.3" transform="translate(0,-.5)"/><rect x="{bx + 96}" y="{by + 16}" width="12" height="8" rx="2" fill="{CYAN}"/>
<text x="{bx + 118}" y="{by + 23}" class="m" font-size="11.5" fill="#cbd5e1">github.com/{D['github']}</text>
<rect x="{bx + 118 + 7.36 * (len(D["github"]) + 11) + 3}" y="{by + 12}" width="1.6" height="14" fill="{CYAN}"><animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" dur="1s" repeatCount="indefinite" calcMode="discrete"/></rect>
<!-- mock page -->
<circle cx="{bx + 330}" cy="{by + 150}" r="120" fill="url(#{p}-gv)"/>
<text x="{bx + 28}" y="{by + 96}" class="m" font-size="11" fill="{VIOLET}">&lt;h1&gt;</text>
<text x="{bx + 28}" y="{by + 130}" class="d" font-weight="700" font-size="34" fill="url(#{p}-tx)">Build it.</text>
<text x="{bx + 28}" y="{by + 164}" class="d" font-weight="700" font-size="34" fill="#f1f5f9">Ship it.</text>
<rect x="{bx + 28}" y="{by + 184}" width="150" height="7" rx="3.5" fill="#ffffff22"/><rect x="{bx + 28}" y="{by + 200}" width="116" height="7" rx="3.5" fill="#ffffff14"/>
<rect x="{bx + 28}" y="{by + 222}" width="86" height="26" rx="13" fill="url(#{p}-hair)"/><text x="{bx + 71}" y="{by + 239}" class="m" font-size="11" font-weight="700" fill="#0d0e16" text-anchor="middle">hire me</text>
<g class="m" font-size="10" fill="{CYAN}" opacity=".9"><text x="{bx + 150}" y="{by + 90}">const</text><text x="{bx + 190}" y="{by + 90}" fill="{PINK}">dev</text></g>
<image class="pop" style="animation-delay:.5s" x="{bx + 190}" y="{by + 40}" width="252" height="302" xlink:href="data:image/png;base64,{b64file(ASSETS / 'dev.png')}"/>
</g>
<rect x="{bx + .6}" y="{by + .6}" width="{bw - 1.2}" height="{bh - 1.2}" rx="15.5" fill="none" stroke="url(#{p}-hair2)" stroke-width="1.2" stroke-opacity=".9"/></g>'''

rows = [('layout', CYAN, 'Frontend that feels alive', 'React, Next.js and motion-first interfaces'),
        ('server', VIOLET, 'Backend that holds up', 'Node.js APIs, databases and auth'),
        ('rocket', PINK, 'Ship end to end', f'From idea to deploy, full stack at {D["company"]}')]
for i, (ic, col, t, s) in enumerate(rows):
    y = 312 + i * 62
    body += f'''<g class="rise" style="animation-delay:{.7 + i * .15}s">
<rect x="28" y="{y}" width="46" height="46" rx="13" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".55"/>
<g transform="translate(40,{y + 12}) scale(1)">{stroke_icon(ic and ICON[ic], col)}</g>
<text x="90" y="{y + 20}" class="d" font-weight="700" font-size="18" fill="#f1f5f9">{t}</text>
<text x="90" y="{y + 40}" class="m" font-size="11.5" fill="#94a3b8">{s}</text></g>'''

# ================================================================ RIGHT: hobby carousel
RX = 512
SEG = 3
LOOP = 12.0
sw = (440 - (SEG - 1) * 8) / SEG
for i in range(SEG):
    x = RX + 24 + i * (sw + 8)
    a, b = i / SEG, (i + 1) / SEG
    if i == 0:
        vs, ks = [0, sw, sw], [0, b, 1]
    else:
        vs, ks = [0, 0, sw, sw], [0, a, b, 1]
    body += (f'<rect x="{x}" y="28" width="{sw}" height="4" rx="2" fill="#ffffff1c"/>'
             f'<rect x="{x}" y="28" width="{sw}" height="4" rx="2" fill="url(#{p}-hair)">'
             f'<animate attributeName="width" values="{";".join(fmt(v) for v in vs)}" keyTimes="{";".join(fmt(k) for k in ks)}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/></rect>')

BX0, BY0, BW, BH = RX + 24, 44, 440, 214
body += f'<defs><clipPath id="{p}-sl"><rect x="{BX0}" y="{BY0}" width="{BW}" height="{BH}" rx="20"/></clipPath>' \
        f'<linearGradient id="{p}-pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".07"/><stop offset="1" stop-color="#ffffff" stop-opacity=".02"/></linearGradient></defs>'
body += f'<rect x="{BX0}" y="{BY0}" width="{BW}" height="{BH}" rx="20" fill="url(#{p}-pg)" stroke="#ffffff14"/>'

cx0 = BX0 + BW / 2  # 756
cy0 = BY0 + BH / 2  # 151


def float_(dy=6, dur=3.2, begin=0):
    return (f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {-dy};0 0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>')


# slide 1: open book
s1 = f'''<g>
<circle cx="{cx0}" cy="{cy0 + 6}" r="86" fill="url(#{p}-gc)"/>
<path d="M{cx0} {cy0 + 52} C{cx0 - 36} {cy0 + 30} {cx0 - 84} {cy0 + 28} {cx0 - 118} {cy0 + 40} V{cy0 - 52} C{cx0 - 84} {cy0 - 64} {cx0 - 36} {cy0 - 60} {cx0} {cy0 - 36}Z" fill="#161a2e" stroke="{CYAN}" stroke-width="2"/>
<path d="M{cx0} {cy0 + 52} C{cx0 + 36} {cy0 + 30} {cx0 + 84} {cy0 + 28} {cx0 + 118} {cy0 + 40} V{cy0 - 52} C{cx0 + 84} {cy0 - 64} {cx0 + 36} {cy0 - 60} {cx0} {cy0 - 36}Z" fill="#1c1833" stroke="{VIOLET}" stroke-width="2"/>
<g stroke="#ffffff30" stroke-width="3" stroke-linecap="round"><path d="M{cx0 - 100} {cy0 - 30}q36-10 80 6M{cx0 - 100} {cy0 - 12}q36-10 80 6M{cx0 - 100} {cy0 + 6}q36-10 80 6M{cx0 + 20} {cy0 - 24}q40-14 80-6M{cx0 + 20} {cy0 - 6}q40-14 80-6"/></g>
<path d="M{cx0 + 70} {cy0 - 54} v34 l10 -8 l10 8 v-38z" fill="{PINK}"/>
<g>{float_(8, 2.8)}<path d="M{cx0 - 98} {cy0 - 70} l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4z" fill="{CYAN}"/></g>
<g>{float_(6, 3.6, .6)}<path d="M{cx0 + 104} {cy0 - 66} l3 7 l7 3 l-7 3 l-3 7 l-3 -7 l-7 -3 l7 -3z" fill="{PINK}"/></g></g>'''

# slide 2: lightbulb + code
s2 = f'''<g>
<circle cx="{cx0}" cy="{cy0 - 8}" r="92" fill="url(#{p}-gp)"><animate attributeName="r" values="86;98;86" dur="3s" repeatCount="indefinite"/></circle>
<path d="M{cx0 - 26} {cy0 + 24} C{cx0 - 26} {cy0 + 6} {cx0 - 52} {cy0 - 4} {cx0 - 52} {cy0 - 36} a52 52 0 0 1 104 0 C{cx0 + 52} {cy0 - 4} {cx0 + 26} {cy0 + 6} {cx0 + 26} {cy0 + 24}z" fill="#241a3d" stroke="{PINK}" stroke-width="2.4"/>
<path d="M{cx0 - 12} {cy0 + 20} l8-30 l8 14 l8-14 l8 30" fill="none" stroke="{CYAN}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round" transform="translate(-4,-10)"/>
<rect x="{cx0 - 24}" y="{cy0 + 28}" width="48" height="9" rx="4.5" fill="#94a3b8"/><rect x="{cx0 - 17}" y="{cy0 + 41}" width="34" height="9" rx="4.5" fill="#64748b"/>
<g stroke="{VIOLET}" stroke-width="3" stroke-linecap="round"><path d="M{cx0 - 82} {cy0 - 44}l-18 -8M{cx0 + 82} {cy0 - 44}l18 -8M{cx0} {cy0 - 100}v-12M{cx0 - 70} {cy0 - 82}l-12 -10M{cx0 + 70} {cy0 - 82}l12 -10"><animate attributeName="stroke-opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></path></g>
<text x="{cx0 - 150}" y="{cy0 + 28}" class="m" font-size="22" font-weight="700" fill="{CYAN}" opacity=".85">&lt;/&gt;</text>
<text x="{cx0 + 96}" y="{cy0 + 36}" class="m" font-size="22" font-weight="700" fill="{PINK}" opacity=".85">{{ }}</text></g>'''

# slide 3: globe + greetings
meridians = ''.join(f'<ellipse cx="{cx0}" cy="{cy0}" rx="{rx}" ry="60" fill="none" stroke="{CYAN}" stroke-opacity=".5"/>' for rx in (22, 42))
lat = ''.join(f'<path d="M{cx0 - w_} {cy0 + dy}h{2 * w_}" stroke="{VIOLET}" stroke-opacity=".5"/>' for dy, w_ in ((-30, 52), (0, 60), (30, 52)))
bubbles = [('Hello', cx0 - 148, cy0 - 62, CYAN), ('Hola', cx0 + 74, cy0 - 74, PINK), ('Bonjour', cx0 + 72, cy0 + 32, VIOLET), ('Shagotom', cx0 - 156, cy0 + 28, CYAN)]
bb = ''
for i, (t, x, y, col) in enumerate(bubbles):
    wd = 16 + len(t) * 7.4
    bb += (f'<g>{float_(6, 3 + i * .4, i * .5)}<rect x="{x}" y="{y}" width="{wd}" height="26" rx="13" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".7"/>'
           f'<text x="{x + wd / 2}" y="{y + 17}" class="m" font-size="11.5" font-weight="700" fill="#f1f5f9" text-anchor="middle">{t}</text></g>')
s3 = f'''<g><circle cx="{cx0}" cy="{cy0}" r="96" fill="url(#{p}-gv)"/>
<circle cx="{cx0}" cy="{cy0}" r="60" fill="#12162a" stroke="url(#{p}-hair)" stroke-width="2.2"/>{meridians}{lat}
<path d="M{cx0} {cy0 - 60}v120" stroke="{CYAN}" stroke-opacity=".5"/>
<path d="M{cx0 - 20} {cy0 - 30} q14 -10 26 0 q10 14 -4 24 q-14 4 -18 -10z" fill="{CYAN}" fill-opacity=".35"/>
<path d="M{cx0 + 8} {cy0 + 10} q14 -8 24 6 q2 16 -12 20 q-14 -6 -12 -26z" fill="{PINK}" fill-opacity=".35"/>
{bb}</g>'''

slides = [
    (s1, 'Reading', 'Stories, docs and long reads that stretch my thinking.'),
    (s2, 'Learning a new thing', 'Pick a topic, build something tiny, repeat.'),
    (s3, 'New languages and cultures', 'Every language is another way of seeing the world.'),
]
for k, (art, title, sub) in enumerate(slides):
    a, b = k / SEG, (k + 1) / SEG
    f = .03
    if k == 0:
        ov, ok_ = [1, 1, 0, 0, 1], [0, b - f, b, 1 - f, 1]
    elif k == SEG - 1:
        ov, ok_ = [0, 0, 1, 1, 0], [0, a - f, a, 1 - f, 1]
    else:
        ov, ok_ = [0, 0, 1, 1, 0, 0], [0, a - f, a, b - f, b, 1]
    if k == 0:
        tv, tk = '30 0;0 0;0 0;30 0', [0, .04, 1 - f, 1]
    else:
        tv, tk = '30 0;30 0;0 0;0 0', [0, a - f, a + .04, 1]
    body += f'''<g opacity="{1 if k == 0 else 0}">
<animate attributeName="opacity" values="{";".join(map(str, ov))}" keyTimes="{";".join(fmt(x) for x in ok_)}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>
<g><animateTransform attributeName="transform" type="translate" values="{tv}" keyTimes="{";".join(fmt(x) for x in tk)}" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>
<g clip-path="url(#{p}-sl)">{art}</g>
<text x="{BX0 + 4}" y="{BY0 + BH + 36}" class="d" font-weight="700" font-size="24" fill="#f1f5f9">{title}</text>
<text x="{BX0 + 4}" y="{BY0 + BH + 58}" class="m" font-size="11.5" fill="#94a3b8">{sub}</text></g></g>'''

# daily rings
body += f'<text x="{BX0 + 4}" y="372" class="m" font-size="10.5" fill="{CYAN}" letter-spacing="2">DAILY RINGS</text><path d="M{BX0 + 100} 368H{BX0 + BW}" stroke="#ffffff18" stroke-dasharray="3 5"/>'
rings = [('Read', 78, CYAN), ('Learn', 64, VIOLET), ('Explore', 52, PINK)]
for i, (lab, pct, col) in enumerate(rings):
    cx = RX + 24 + 70 + i * 150
    cy = 428
    body += f'''<g class="rise" style="animation-delay:{1 + i * .15}s"><circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="#ffffff14" stroke-width="7"/>
<circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="{100 - pct}" transform="rotate(-90 {cx} {cy})">
<animate attributeName="stroke-dashoffset" values="100;{100 - pct};{100 - pct};100" keyTimes="0;.45;.9;1" dur="6s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines=".2 .8 .2 1;0 0 1 1;.4 0 1 1"/></circle>
<text x="{cx}" y="{cy + 5}" class="m" font-size="14" font-weight="700" fill="#f1f5f9" text-anchor="middle">{pct}%</text>
<text x="{cx}" y="{cy + 54}" class="m" font-size="11" fill="#94a3b8" text-anchor="middle">{lab}</text></g>'''

open(ASSETS / 'about-life.svg', 'w').write(wrap(p, W, H, body, 'About: capabilities, hobbies carousel and daily rings'))
print('about-life.svg KB', (ASSETS / 'about-life.svg').stat().st_size // 1024)
