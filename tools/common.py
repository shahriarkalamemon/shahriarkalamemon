import base64, ctypes, io, math, os, re, sys, types, tempfile
from pathlib import Path

ROOT = Path('/home/claude/profile')
ASSETS = ROOT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
UP = Path('/mnt/user-data/uploads')
FONTS = Path('/mnt/skills/examples/canvas-design/canvas-fonts')
ICONS = Path('/usr/local/lib/python3.12/dist-packages/material/templates/.icons/simple')

# ------------------------------------------------------------------ profile data
# Edit these once; every file picks them up.
D = dict(
    name1='SHAHRIAR', name2='KALAM EMON',
    role='Full Stack Web Developer',
    github='shahriarkalamemon', github_url='https://github.com/shahriarkalamemon',
    email='shahriarkalamemon122005@gmail.com',
    city='Sylhet City', company='Codejogot',
    # PLACEHOLDERS - replace with your real numbers / repo names
    repos=12, stars=48, commits=640,
    top_repos=[('project-alpha', 21), ('project-bravo', 14), ('project-charlie', 9),
               ('project-delta', 6), ('project-echo', 3)],
)

# ------------------------------------------------------------------ brotli shim (libbrotli via ctypes)
_enc = ctypes.CDLL('libbrotlienc.so.1')
_dec = ctypes.CDLL('libbrotlidec.so.1')


def _compress(data, mode=0, quality=11, lgwin=22, lgblock=0):
    data = bytes(data)
    n = ctypes.c_size_t(len(data) + len(data) // 2 + 4096)
    buf = ctypes.create_string_buffer(n.value)
    ok = _enc.BrotliEncoderCompress(ctypes.c_int(quality), ctypes.c_int(lgwin), ctypes.c_int(mode),
                                    ctypes.c_size_t(len(data)), data, ctypes.byref(n), buf)
    assert ok, 'brotli compress failed'
    return buf.raw[:n.value]


def _decompress(data):
    data = bytes(data)
    size = max(len(data) * 8, 1 << 16)
    for _ in range(8):
        n = ctypes.c_size_t(size)
        buf = ctypes.create_string_buffer(size)
        if _dec.BrotliDecoderDecompress(ctypes.c_size_t(len(data)), data, ctypes.byref(n), buf) == 1:
            return buf.raw[:n.value]
        size *= 4
    raise RuntimeError('brotli decompress failed')


_m = types.ModuleType('brotli')
_m.compress, _m.decompress = _compress, _decompress
_m.MODE_GENERIC, _m.MODE_TEXT, _m.MODE_FONT = 0, 1, 2
sys.modules['brotli'] = _m

from fontTools import subset  # noqa: E402

UNICODES = list(range(0x20, 0x7F)) + [0xB7, 0x2014, 0x2013, 0x2019, 0x2192, 0x2022]


def font_b64(path):
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['kern', 'liga', 'calt', 'tnum', 'zero']
    opts.name_IDs = [1, 2]
    opts.notdef_outline = True
    f = subset.load_font(str(path), opts)
    s = subset.Subsetter(opts)
    s.populate(unicodes=UNICODES)
    s.subset(f)
    tmp = tempfile.NamedTemporaryFile(suffix='.woff2', delete=False)
    tmp.close()
    subset.save_font(f, tmp.name, opts)
    b = Path(tmp.name).read_bytes()
    os.unlink(tmp.name)
    return base64.b64encode(b).decode(), len(b)


_FONT_CACHE = {}


def font_css():
    if 'css' in _FONT_CACHE:
        return _FONT_CACHE['css']
    spec = [('Outfit', 400, 'Outfit-Regular.ttf'), ('Outfit', 700, 'Outfit-Bold.ttf'),
            ('JetBrains Mono', 400, 'JetBrainsMono-Regular.ttf'), ('JetBrains Mono', 700, 'JetBrainsMono-Bold.ttf')]
    css = ''
    for fam, wt, fn in spec:
        b, n = font_b64(FONTS / fn)
        css += (f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;"
                f"src:url(data:font/woff2;base64,{b}) format('woff2')}}")
    _FONT_CACHE['css'] = css
    return css


# ------------------------------------------------------------------ icons
def icon_path(slug):
    t = (ICONS / f'{slug}.svg').read_text()
    return re.search(r'<path d="([^"]+)"', t).group(1)


def b64file(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


# ------------------------------------------------------------------ shared svg bits
CYAN, VIOLET, PINK = '#22d3ee', '#a78bfa', '#f472b6'
BG = '#0d0e16'

BASE_CSS = """
.d{font-family:'Outfit',system-ui,-apple-system,'Segoe UI',sans-serif}
.m{font-family:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@keyframes rise{from{opacity:0;transform:translateY(14px)}}
@keyframes pop{from{opacity:0;transform:scale(.92)}}
@keyframes slide{from{opacity:0;transform:translateX(-18px)}}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(7px)}}
.rise{animation:rise .9s cubic-bezier(.2,.8,.2,1) both}
.pop{animation:pop .8s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:center}
.slide{animation:slide .8s cubic-bezier(.2,.8,.2,1) both}
.nudge{animation:nudge 1.8s ease-in-out infinite}
"""


def common_defs(p):
    return f"""
<linearGradient id="{p}-hair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="{p}-hair2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PINK}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="{p}-sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".06"/><stop offset=".5" stop-color="#fff" stop-opacity=".0"/></linearGradient>
<pattern id="{p}-dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r=".9" fill="#fff" fill-opacity=".07"/></pattern>
<radialGradient id="{p}-gc"><stop offset="0" stop-color="{CYAN}" stop-opacity=".30"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="{p}-gv"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".30"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="{p}-gp"><stop offset="0" stop-color="{PINK}" stop-opacity=".26"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
"""


def card(p, x, y, w, h, r=26, glow=True):
    s = f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{BG}"/>'
    if glow:
        s += (f'<clipPath id="{p}-cc{x}{y}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
              f'<g clip-path="url(#{p}-cc{x}{y})">'
              f'<ellipse cx="{x + w * .12}" cy="{y + h * .1}" rx="{w * .38}" ry="{h * .5}" fill="url(#{p}-gc)"/>'
              f'<ellipse cx="{x + w * .9}" cy="{y + h * .95}" rx="{w * .38}" ry="{h * .5}" fill="url(#{p}-gp)"/>'
              f'<ellipse cx="{x + w * .6}" cy="{y + h * .3}" rx="{w * .3}" ry="{h * .4}" fill="url(#{p}-gv)"/></g>')
    s += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{p}-dots)"/>'
          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{p}-sheen)"/>'
          f'<rect x="{x + .6}" y="{y + .6}" width="{w - 1.2}" height="{h - 1.2}" rx="{r - .6}" fill="none" '
          f'stroke="url(#{p}-hair)" stroke-width="1.2" stroke-opacity=".85"/></g>')
    return s


def wrap(p, W, H, body, label, defs_extra='', css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">'
            f'<style>{font_css()}{BASE_CSS}{css}</style>'
            f'<defs>{common_defs(p)}{defs_extra}</defs>{body}</svg>')


def ease_out(t):
    return 1 - (1 - t) ** 3


def fmt(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')
