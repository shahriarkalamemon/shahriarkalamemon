from common import *

p = 's'
W, H = 1000, 732
CX, CY = 500, 222
CORE_R = 36
body = card(p, 0, 0, W, 444, 30) + card(p, 0, 464, W, 268, 30)

ICON_SZ = 38  # base badge size


def rot(x, y, deg):
    a = math.radians(deg)
    return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)


def orbit_pt(rx, ry, tilt, th):
    x, y = rot(rx * math.cos(th), ry * math.sin(th), tilt)
    return x, y, math.sin(th)  # z: >0 front


def nested_icon(slug, color, samples, base, ids=None, size=ICON_SZ, depth=True):
    """samples: list of (x,y,z) centre positions (+ optional scale override). returns svg."""
    d = icon_path(slug)

    def vals(fn):
        return ';'.join(fmt(fn(s)) for s in samples)

    def sc(s):
        return (1 + .16 * s[2]) if depth else 1.0

    x0, y0, z0 = samples[0]
    s0 = sc(samples[0])
    return (f'<svg x="{fmt(x0 - size * s0 / 2)}" y="{fmt(y0 - size * s0 / 2)}" width="{fmt(size * s0)}" height="{fmt(size * s0)}" '
            f'viewBox="-6 -6 36 36" overflow="visible" opacity="{fmt(.62 + .38 * (z0 + 1) / 2)}">'
            f'<circle cx="12" cy="12" r="17" fill="{BG}" stroke="{color}" stroke-opacity=".75" stroke-width="1"/>'
            f'<circle cx="12" cy="12" r="17" fill="{color}" fill-opacity=".10"/>'
            f'<path d="{d}" fill="{color}"/>'
            f'<animate attributeName="x" values="{vals(lambda s: s[0] - size * sc(s) / 2)}" dur="{base}s" begin="0s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{vals(lambda s: s[1] - size * sc(s) / 2)}" dur="{base}s" begin="0s" repeatCount="indefinite"/>'
            f'<animate attributeName="width" values="{vals(lambda s: size * sc(s))}" dur="{base}s" begin="0s" repeatCount="indefinite"/>'
            f'<animate attributeName="height" values="{vals(lambda s: size * sc(s))}" dur="{base}s" begin="0s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{vals(lambda s: .62 + .38 * (s[2] + 1) / 2)}" dur="{base}s" begin="0s" repeatCount="indefinite"/></svg>')


# ---------------------------------------------------------------- orbits
orbits = [
    dict(rx=178, ry=80, tilt=-14, T=20, dir=1, col=CYAN, icons=['nodedotjs', 'express', 'postgresql', 'git'], S=240),
    dict(rx=282, ry=126, tilt=16, T=32, dir=-1, col=VIOLET, icons=['react', 'tailwindcss', 'mongodb', 'prisma'], S=480),
    dict(rx=376, ry=150, tilt=-6, T=48, dir=1, col=PINK, icons=['docker', 'vercel', 'figma', 'firebase', 'python'], S=288),
]

defs = f'''<radialGradient id="{p}-core" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#ffffff"/><stop offset=".25" stop-color="{CYAN}"/><stop offset=".65" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></radialGradient>
<radialGradient id="{p}-halo"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".18"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<filter id="{p}-blur" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="2.2"/></filter>'''

body += f'<text x="32" y="46" class="m" font-size="11" letter-spacing="2.4" fill="{CYAN}">// MY STACK</text>'
body += f'<text x="32" y="68" class="d" font-weight="700" font-size="22" fill="#f1f5f9">Tools I orbit every day</text>'

# orbit rings
for o in orbits:
    body += (f'<g transform="translate({CX},{CY}) rotate({o["tilt"]})"><ellipse rx="{o["rx"]}" ry="{o["ry"]}" fill="none" stroke="{o["col"]}" stroke-opacity=".28" stroke-dasharray="2 7" stroke-linecap="round"/></g>')

# core
body += f'''<circle cx="{CX}" cy="{CY}" r="86" fill="url(#{p}-halo)"><animate attributeName="r" values="80;96;80" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;1;.8" dur="4s" repeatCount="indefinite"/></circle>
<circle cx="{CX}" cy="{CY}" r="{CORE_R}" fill="url(#{p}-core)"/>
<circle cx="{CX}" cy="{CY}" r="{CORE_R}" fill="none" stroke="#fff" stroke-opacity=".35"/>
<text x="{CX}" y="{CY + 7}" class="m" font-weight="700" font-size="20" fill="{BG}" text-anchor="middle">&lt;/&gt;</text>'''

min_icon, min_moon = 1e9, 1e9
react_info = None
icon_svgs = []
for oi, o in enumerate(orbits):
    n, S, T = len(o['icons']), o['S'], o['T']
    for k, slug in enumerate(o['icons']):
        ph = 2 * math.pi * k / n + (0.0 if slug != 'react' else 0.0)
        samples = []
        for s in range(S + 1):
            th = ph + o['dir'] * 2 * math.pi * s / S
            x, y, z = orbit_pt(o['rx'], o['ry'], o['tilt'], th)
            samples.append((CX + x, CY + y, z * o['dir'] * o['dir']))
            min_icon = min(min_icon, math.hypot(x, y) - ICON_SZ * 1.16 / 2)
        if slug == 'react':
            react_info = (o, samples, T, S, ph)
        else:
            icon_svgs.append(nested_icon(slug, o['col'], samples, T))

# react + moons
o, rs, T, S, ph = react_info
moons = [dict(slug='typescript', r=44, per=4.0, dir=1, tilt=-20, col=CYAN), dict(slug='nextdotjs', r=60, per=6.4, dir=-1, tilt=24, col=PINK)]
MSZ = 20
moon_svgs = []
for m in moons:
    ms = []
    for s in range(S + 1):
        t = T * s / S
        th = m['dir'] * 2 * math.pi * t / m['per']
        mx, my = rot(m['r'] * math.cos(th), m['r'] * .58 * math.sin(th), m['tilt'])
        z = math.sin(th)
        ms.append((rs[s][0] + mx, rs[s][1] + my, z))
        min_moon = min(min_moon, math.hypot(rs[s][0] + mx - CX, rs[s][1] + my - CY) - MSZ * 1.16 / 2)
    moon_svgs.append(nested_icon(m['slug'], m['col'], ms, T, None, size=MSZ))
    # faint moon orbit ring following react
ring = ''
for m in moons:
    ring += (f'<ellipse rx="{m["r"]}" ry="{fmt(m["r"] * .58)}" fill="none" stroke="{m["col"]}" stroke-opacity=".30" stroke-dasharray="2 5" transform="rotate({m["tilt"]})">'
             f'</ellipse>')
# the ring group follows react: animate group translate through sampled values
follow = ';'.join(f'{fmt(s[0])} {fmt(s[1])}' for s in rs)
body += (f'<g transform="translate({fmt(rs[0][0])},{fmt(rs[0][1])})"><animateTransform attributeName="transform" type="translate" values="{follow}" dur="{T}s" begin="0s" repeatCount="indefinite"/>{ring}</g>')
body += ''.join(icon_svgs)
body += nested_icon('react', VIOLET, rs, T, None, size=ICON_SZ + 6)
body += ''.join(moon_svgs)

CLEAR = min(min_icon, min_moon) - CORE_R
print(f'min icon-to-core gap {min_icon - CORE_R:.1f}px, min moon-to-core gap {min_moon - CORE_R:.1f}px')
assert min_icon - CORE_R > 14 and min_moon - CORE_R > 14, 'overlap with core'

# ---------------------------------------------------------------- chip grid
groups = [
    ('FRONTEND', CYAN, [('react', 'React'), ('nextdotjs', 'Next.js'), ('typescript', 'TypeScript'), ('tailwindcss', 'Tailwind CSS'), ('html5', 'HTML5')]),
    ('MOTION &amp; 3D', VIOLET, [('gsap', 'GSAP'), ('framer', 'Framer Motion'), ('threedotjs', 'Three.js'), ('blender', 'Blender')]),
    ('DATA', PINK, [('postgresql', 'PostgreSQL'), ('mongodb', 'MongoDB'), ('prisma', 'Prisma'), ('redis', 'Redis')]),
    ('AI', CYAN, [('anthropic', 'Claude API'), ('langchain', 'LangChain'), ('huggingface', 'Hugging Face'), ('tensorflow', 'TensorFlow')]),
]
STEP = .4
total = sum(len(g[2]) for g in groups)
LOOPC = total * STEP + 1.0
order = []
rows = max(len(g[2]) for g in groups)
for j in range(rows):
    for i, g in enumerate(groups):
        if j < len(g[2]):
            order.append((i, j))
idx = {k: n for n, k in enumerate(order)}
colw, gap = 218, 24
x_start = (W - (4 * colw + 3 * gap)) / 2
for i, (title, col, chips) in enumerate(groups):
    gx = x_start + i * (colw + gap)
    body += (f'<g class="rise" style="animation-delay:{.2 + i * .1}s"><circle cx="{gx + 5}" cy="{464 + 38}" r="4" fill="{col}"/>'
             f'<text x="{gx + 18}" y="{464 + 42}" class="m" font-size="11.5" font-weight="700" letter-spacing="2.2" fill="#e2e8f0">{title}</text>'
             f'<path d="M{gx} {464 + 54}H{gx + colw}" stroke="#ffffff14"/></g>')
    for j, (slug, label) in enumerate(chips):
        cy = 464 + 68 + j * 38
        cw_ = min(colw, 46 + len(label) * 7.4)
        t0 = idx[(i, j)] * STEP
        kt = [0, t0 / LOOPC, (t0 + .15) / LOOPC, (t0 + .5) / LOOPC, (t0 + 1.0) / LOOPC, 1]
        kt = [min(1, max(0, k)) for k in kt]
        for q in range(1, len(kt)):
            kt[q] = max(kt[q], kt[q - 1])
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{";".join(fmt(k) for k in kt)}" dur="{LOOPC}s" begin="0s" repeatCount="indefinite"/>')
        body += f'''<g class="rise" style="animation-delay:{.3 + i * .08 + j * .06}s">
<rect x="{gx}" y="{cy}" width="{cw_}" height="30" rx="15" fill="#ffffff08" stroke="url(#{p}-hair)" stroke-opacity=".28"/>
<g opacity="0"><rect x="{gx}" y="{cy}" width="{cw_}" height="30" rx="15" fill="none" stroke="{col}" stroke-width="4" filter="url(#{p}-blur)" opacity=".8"/>
<rect x="{gx}" y="{cy}" width="{cw_}" height="30" rx="15" fill="none" stroke="url(#{p}-hair)" stroke-width="1.6"/>{anim}</g>
<g transform="translate({gx + 13},{cy + 8}) scale(.58)"><path d="{icon_path(slug)}" fill="{col}"/></g>
<text x="{gx + 33}" y="{cy + 19.5}" class="m" font-size="12" fill="#e2e8f0">{label}</text></g>'''

open(ASSETS / 'stack.svg', 'w').write(wrap(p, W, H, body, 'Tech stack: orbiting icons around a core and grouped skill chips', defs))
print('stack.svg KB', (ASSETS / 'stack.svg').stat().st_size // 1024)
