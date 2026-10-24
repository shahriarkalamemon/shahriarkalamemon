import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from common import *

lap = Image.open(UP / 'Friendly_Anime_Developer_with_Laptop.png').convert('RGBA')
ptr = Image.open(UP / 'Neon_Anime_GitHub_Promo_Sticker.png').convert('RGBA')
print('alpha laptop', lap.getchannel('A').getextrema(), 'pointing', ptr.getchannel('A').getextrema())

# ------------------------------------------------------------ hero frames (stand-in clip made from the portrait)
FW, FH, S = 340, 376, 2
N = 20
cyan, violet, pink = np.array([34, 211, 238]), np.array([167, 139, 250]), np.array([244, 114, 182])
bbox = lap.getchannel('A').getbbox()
lapc = lap.crop(bbox)
rng = random.Random(7)
parts = [(rng.random(), rng.random(), .15 + rng.random() * .35, rng.choice([0, 1, 2]), 2 + rng.random() * 3) for _ in range(18)]
yy, xx = np.mgrid[0:FH * S, 0:FW * S].astype(float)
frames = []
for k in range(N):
    t = k / (N - 1)
    base = np.zeros((FH * S, FW * S, 3), float) + np.array([13, 14, 22])
    # drifting aurora glow
    for (cx, cy, col, R, a) in [(.5 + .12 * math.sin(t * 3), .78, cyan, .75, .55), (.25 + .3 * t, .35, violet, .6, .4), (.8 - .25 * t, .55, pink, .5, .3)]:
        d = np.sqrt(((xx / (FW * S) - cx)) ** 2 + ((yy / (FH * S) - cy)) ** 2) / R
        w = np.clip(1 - d, 0, 1) ** 2 * a
        base += (col - base) * w[..., None] * .55
    img = Image.fromarray(np.clip(base, 0, 255).astype('uint8')).convert('RGBA')
    # character with slow push-in + float
    sc = 1.0 + .07 * ease_out(t)
    cw = int(FW * S * .98 * sc)
    ch = int(lapc.height * cw / lapc.width)
    c = lapc.resize((cw, ch), Image.LANCZOS)
    ox = (FW * S - cw) // 2
    oy = FH * S - ch + int(10 * S * ease_out(t)) - int(4 * S * math.sin(t * math.pi))
    img.alpha_composite(c, (ox, oy))
    # rising particles
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    for (px, py, sp, ci, r) in parts:
        x = px * FW * S
        y = ((py - t * sp * 1.6) % 1.0) * FH * S
        col = [CYAN, VIOLET, PINK][ci]
        rgb = tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))
        dr.ellipse([x - r * S, y - r * S, x + r * S, y + r * S], fill=rgb + (150,))
    ov = ov.filter(ImageFilter.GaussianBlur(1.2))
    img.alpha_composite(ov)
    # diagonal light sweep
    sweep = np.exp(-(((xx + yy * .45) / (FW * S) - (t * 1.7 - .3)) ** 2) / .006) * .16
    arr = np.asarray(img.convert('RGB')).astype(float)
    arr += sweep[..., None] * 255
    img = Image.fromarray(np.clip(arr, 0, 255).astype('uint8'))
    img = img.resize((FW, FH), Image.LANCZOS)
    path = ASSETS / f'f{k:02d}.jpg'
    img.save(path, quality=80, optimize=True, progressive=False)
    frames.append(path)
print('frames', N, 'total KB', sum(p.stat().st_size for p in frames) // 1024)

# ------------------------------------------------------------ browser illustration (character on gradient, transparent PNG)
w = 300
h = int(lap.height * w / lap.width)
lap.resize((w, h), Image.LANCZOS).save(ASSETS / 'dev.png', optimize=True)

# ------------------------------------------------------------ badge portrait (face crop on dark gradient)
face = lap.crop((290, 0, 800, 510))
bgp = Image.new('RGBA', face.size, (20, 21, 34, 255))
g = np.zeros((face.height, face.width, 3), float)
yy2, xx2 = np.mgrid[0:face.height, 0:face.width]
dd = np.sqrt((xx2 / face.width - .5) ** 2 + (yy2 / face.height - .55) ** 2)
base = np.array([20, 21, 34]) + (violet - np.array([20, 21, 34])) * np.clip(1 - dd / .7, 0, 1)[..., None] ** 2 * .6
bgp = Image.fromarray(base.astype('uint8')).convert('RGBA')
bgp.alpha_composite(face)
bgp.resize((300, 300), Image.LANCZOS).convert('RGB').save(ASSETS / 'portrait.png', optimize=True)

# ------------------------------------------------------------ pointing character
ph = 520
pw = int(ptr.width * ph / ptr.height)
ptr.resize((pw, ph), Image.LANCZOS).save(ASSETS / 'point.png', optimize=True)
print('sizes KB', {p.name: p.stat().st_size // 1024 for p in ASSETS.glob('*.png')}, 'point size', pw, ph, 'dev', w, h)
