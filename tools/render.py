import sys, re
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path('/home/claude/profile')
SHOTS = ROOT / 'shots'
SHOTS.mkdir(exist_ok=True)


def render(name, times, static=True, scale=1):
    path = ROOT / 'assets' / f'{name}.svg'
    txt = path.read_text()
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', txt)
    W, H = int(m.group(1)), int(m.group(2))
    outs = []
    errs = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=scale)
        pg.on('console', lambda msg: errs.append(msg.text) if msg.type == 'error' else None)
        pg.on('requestfailed', lambda r: errs.append('REQFAIL ' + r.url[:80]))
        pg.on('request', lambda r: errs.append('NETWORK ' + r.url[:80]) if not r.url.startswith(('data:', 'file:')) else None)
        for t in times:
            pg.goto(f'file://{path}')
            pg.evaluate('document.fonts.ready')
            pg.evaluate('''t=>{const s=document.documentElement;s.pauseAnimations();s.setCurrentTime(t);
              document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});}''', t)
            pg.wait_for_timeout(150)
            o = SHOTS / f'{name}_{t:g}.png'
            pg.screenshot(path=str(o))
            outs.append(o)
        if static:
            pg.goto(f'file://{path}')
            pg.evaluate('document.fonts.ready')
            pg.evaluate('''()=>{document.querySelectorAll('animate,animateTransform,set,animateMotion').forEach(e=>e.remove());
               const st=document.createElementNS('http://www.w3.org/2000/svg','style');st.textContent='*{animation:none!important}';
               document.documentElement.appendChild(st);}''')
            pg.wait_for_timeout(150)
            o = SHOTS / f'{name}_static.png'
            pg.screenshot(path=str(o))
            outs.append(o)
        b.close()
    return outs, errs


def sheet(name, outs, cols=2, width=700):
    ims = [Image.open(o).convert('RGB') for o in outs]
    r = width / ims[0].width
    ims = [i.resize((width, int(i.height * r))) for i in ims]
    rows = (len(ims) + cols - 1) // cols
    h = ims[0].height
    S = Image.new('RGB', (cols * width, rows * h), (40, 40, 50))
    for i, im in enumerate(ims):
        S.paste(im, ((i % cols) * width, (i // cols) * h))
    o = SHOTS / f'{name}_sheet.png'
    S.save(o)
    return o


if __name__ == '__main__':
    name = sys.argv[1]
    times = [float(x) for x in sys.argv[2].split(',')]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 700
    outs, errs = render(name, times)
    print('errors:', errs[:10])
    print(sheet(name, outs, cols=2, width=width))
