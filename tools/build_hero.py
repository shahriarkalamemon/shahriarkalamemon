from common import *

p = 'h'
W, H = 1100, 420
VX, VY, VW, VH = 700, 24, 340, 376
N = 20
LOOP = 4.0
PLAY = 2.6
fr = PLAY / LOOP  # 0.65


def anim(attr, values, kt=None, dur=LOOP, extra=''):
    v = ';'.join(str(x) for x in values)
    k = f' keyTimes="{";".join(fmt(x) for x in kt)}"' if kt else ''
    return f'<animate attributeName="{attr}" values="{v}"{k} dur="{dur}s" begin="0s" repeatCount="indefinite" {extra}/>'


body = card(p, 0, 0, W, H, 30)

# ---------------------------------------------------------------- left column
# pill
body += f'''<g class="rise" style="animation-delay:.1s">
<rect x="48" y="40" width="206" height="32" rx="16" fill="#ffffff08" stroke="url(#{p}-hair)" stroke-opacity=".7"/>
<circle cx="68" cy="56" r="4" fill="{CYAN}"/>
<circle cx="68" cy="56" r="4" fill="none" stroke="{CYAN}" stroke-width="1.5"><animate attributeName="r" values="4;11;4" dur="2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".9;0;.9" dur="2s" repeatCount="indefinite"/></circle>
<text x="86" y="60" class="m" font-size="12" font-weight="700" fill="#e2e8f0" letter-spacing="1.4">OPEN TO COLLABS</text></g>'''

# typed line (clip reveals 13 chars, mono 20px => 12px/char)
chars = 13
cw = 12.8
vals = ""
body += f'''<clipPath id="{p}-type"><rect x="48" y="90" width="{cw * chars}" height="34">
<animate attributeName="width" values="0;0;{vals}" keyTimes="0;.001;{';'.join(fmt(.001 + .999 * (i / chars)) for i in range(1, chars + 1)).replace(';', ';', 1)}" dur="1.8s" begin="0s" fill="freeze" calcMode="discrete" additive="replace"/></rect></clipPath>'''
# (simpler, valid discrete timeline built explicitly)
steps = [0] + [fmt(cw * i) for i in range(1, chars + 1)]
kts = [0] + [(.12 + .88 * i / chars) for i in range(1, chars + 1)]
body = body.replace(body[body.index(f'<clipPath id="{p}-type">'):], '')
body += f'''<clipPath id="{p}-type"><rect x="48" y="88" width="{cw * chars}" height="36">
<animate attributeName="width" values="0;{';'.join(str(s) for s in steps[1:])}" keyTimes="0;{';'.join(fmt(k) for k in kts[1:])}" dur="1.6s" begin="0s" fill="freeze" calcMode="discrete"/></rect></clipPath>
<text x="48" y="112" class="m" font-size="20" fill="{CYAN}" clip-path="url(#{p}-type)">Hi there, I'm</text>
<rect x="{48 + cw * chars + 3}" y="95" width="10" height="20" fill="{CYAN}"><animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" dur="1s" repeatCount="indefinite" calcMode="discrete"/></rect>'''

# name with rising mask + animated gradient
body += f'''<defs>
<linearGradient id="{p}-name" gradientUnits="userSpaceOnUse" x1="48" y1="0" x2="548" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;500 0" dur="6s" repeatCount="indefinite"/></linearGradient>
<clipPath id="{p}-rise"><rect x="40" y="132" width="600" height="156">
<animate attributeName="y" values="288;288;132" keyTimes="0;.4;1" dur="2.4s" begin="0s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;.2 .8 .2 1"/>
<animate attributeName="height" values="0;0;156" keyTimes="0;.4;1" dur="2.4s" begin="0s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;.2 .8 .2 1"/></rect></clipPath></defs>
<g clip-path="url(#{p}-rise)">
<text x="46" y="198" class="d" font-weight="700" font-size="76" letter-spacing="1" fill="url(#{p}-name)">{D['name1']}</text>
<text x="46" y="272" class="d" font-weight="700" font-size="76" letter-spacing="1" fill="url(#{p}-name)">{D['name2']}</text></g>'''

# cycling roles
roles = [D['role'], 'React + Next.js + TypeScript builder', 'Learner of new things, languages and cultures']
cyc = 9.0
t_roles = ''
for i, r in enumerate(roles):
    a, b = i / 3, (i + 1) / 3
    if i == 0:
        vals_, kt_ = [1, 1, 0, 0, 1], [0, b - .03, b, 1 - .03, 1]
    else:
        vals_, kt_ = [0, 0, 1, 1, 0, 0], [0, a - .0001, a + .03, b - .03, b, 1]
        if i == 2:
            vals_, kt_ = [0, 0, 1, 1, 0], [0, a, a + .03, 1 - .03, 1]
    t_roles += (f'<text x="48" y="318" class="d" font-size="25" fill="#e5e7eb" opacity="{1 if i == 0 else 0}">'
                f'<tspan fill="{PINK}" class="m" font-size="20">&gt; </tspan>{r}'
                f'<animate attributeName="opacity" values="{";".join(map(str, vals_))}" keyTimes="{";".join(fmt(k) for k in kt_)}" dur="{cyc}s" begin="0s" repeatCount="indefinite"/></text>')
body += f'<g class="rise" style="animation-delay:1.9s">{t_roles}</g>'

body += f'''<g class="rise" style="animation-delay:2.1s"><text x="48" y="352" class="d" font-size="16" fill="#94a3b8">Building fast, polished web apps end to end, from pixel-tight UI to resilient APIs.</text></g>'''

# meta row with drawn icons
ic = {
    'pin': '<path d="M7 1C4.2 1 2 3.2 2 6c0 3.6 5 8 5 8s5-4.4 5-8c0-2.8-2.2-5-5-5z"/><circle cx="7" cy="6" r="1.8"/>',
    'bld': '<rect x="2" y="2" width="10" height="11" rx="1.5"/><path d="M5 5h1M8 5h1M5 8h1M8 8h1M6 13v-2h2v2"/>',
    'star': '<path d="M7 1.5l1.7 3.6 3.9.5-2.9 2.7.8 3.9L7 10.3 3.5 12.2l.8-3.9L1.4 5.6l3.9-.5z"/>',
}
meta = [('pin', D['city'], 48), ('bld', D['company'], 190), ('star', f"{D['repos']} repos · {D['stars']} stars", 322)]
mm = ''
for k, (i_, txt, x) in enumerate(meta):
    mm += (f'<g class="rise" style="animation-delay:{2.3 + k * .15}s"><g transform="translate({x},378)" fill="none" stroke="{CYAN if k == 0 else VIOLET if k == 1 else PINK}" '
           f'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{ic[i_]}</g>'
           f'<text x="{x + 22}" y="390" class="m" font-size="12.5" fill="#cbd5e1">{txt}</text></g>')
body += mm

# ---------------------------------------------------------------- viewfinder video
body += f'''<defs>
<radialGradient id="{p}-vm" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff"/><stop offset=".62" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="{p}-mask" maskUnits="userSpaceOnUse" x="{VX}" y="{VY}" width="{VW}" height="{VH}"><rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="url(#{p}-vm)"/></mask></defs>
<g mask="url(#{p}-mask)"><g>
<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.925;1" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/>'''
for k in range(N):
    a = k / N * fr
    b = (k + 1) / N * fr
    img = f'<image x="{VX}" y="{VY}" width="{VW}" height="{VH}" preserveAspectRatio="none" xlink:href="data:image/jpeg;base64,{b64file(ASSETS / f"f{k:02d}.jpg")}" visibility="{"visible" if k == N - 1 else "hidden"}">'
    if k == 0:
        vs, ks = 'visible;hidden', [0, b]
    elif k == N - 1:
        vs, ks = 'hidden;visible', [0, a]
    else:
        vs, ks = 'hidden;visible;hidden', [0, a, b]
    img += f'<animate attributeName="visibility" values="{vs}" keyTimes="{";".join(fmt(x) for x in ks)}" calcMode="discrete" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/></image>'
    body += img
body += '</g></g>'

# brackets
L = 26
x0, y0, x1, y1 = VX - 12, VY - 10, VX + VW + 12, VY + VH + 10
br = [f'M{x0},{y0 + L}V{y0}H{x0 + L}', f'M{x1 - L},{y0}H{x1}V{y0 + L}', f'M{x1},{y1 - L}V{y1}H{x1 - L}', f'M{x0 + L},{y1}H{x0}V{y1 - L}']
for i, d in enumerate(br):
    body += (f'<path d="{d}" fill="none" stroke="{CYAN}" stroke-width="2.4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">'
             f'<animate attributeName="stroke-dashoffset" values="1;1;0" keyTimes="0;{fmt(.1 + i * .1)};1" dur="1.4s" begin="0s" fill="freeze"/></path>')

# REC
body += f'''<g class="rise" style="animation-delay:.6s"><circle cx="{VX + 14}" cy="{VY + 12}" r="5" fill="#ef4444"><animate attributeName="opacity" values="1;.15;1" keyTimes="0;.5;1" dur="1.2s" repeatCount="indefinite" calcMode="discrete"/></circle>
<text x="{VX + 26}" y="{VY + 16}" class="m" font-size="11" font-weight="700" fill="#e2e8f0" letter-spacing="1.5">REC</text>
<text x="{VX + VW - 8}" y="{VY + 16}" class="m" font-size="10.5" fill="#94a3b8" text-anchor="end">4K · 24FPS · AURORA</text></g>'''
# filename + timecode
body += f'<text x="{VX + 6}" y="{VY + VH - 22}" class="m" font-size="11" fill="#94a3b8">emon_intro.mov</text>'
for s in range(5):
    vis = 'visible' if s == 4 else 'hidden'
    a, b = s / 4, (s + 1) / 4
    vs, ks = ('visible;hidden', [0, b]) if s == 0 else (('hidden;visible', [0, a]) if s == 4 else ('hidden;visible;hidden', [0, a, b]))
    body += (f'<text x="{VX + VW - 6}" y="{VY + VH - 22}" class="m" font-size="11" fill="{CYAN}" text-anchor="end" visibility="{vis}">00:0{s}'
             f'<animate attributeName="visibility" values="{vs}" keyTimes="{";".join(fmt(x) for x in ks)}" calcMode="discrete" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/></text>')
# scrubber
body += f'''<rect x="{VX}" y="{VY + VH - 10}" width="{VW}" height="4" rx="2" fill="#ffffff18"/>
<rect x="{VX}" y="{VY + VH - 10}" width="{VW}" height="4" rx="2" fill="url(#{p}-hair)">
<animate attributeName="width" values="0;{VW};{VW}" keyTimes="0;{fr};1" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/></rect>
<circle cx="{VX + VW}" cy="{VY + VH - 8}" r="5.5" fill="#fff"><animate attributeName="cx" values="{VX};{VX + VW};{VX + VW}" keyTimes="0;{fr};1" dur="{LOOP}s" begin="0s" repeatCount="indefinite"/></circle>'''

open(ROOT / 'assets' / 'hero.svg', 'w').write(wrap(p, W, H, body, 'Shahriar Kalam Emon, Full Stack Web Developer. Animated hero.'))
print('hero.svg KB', (ROOT / 'assets' / 'hero.svg').stat().st_size // 1024)
