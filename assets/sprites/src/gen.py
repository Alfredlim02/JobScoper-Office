from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 16, 22  # cell; row 0 blank so step frames can bob

def hx(s):
    s = s.lstrip('#')
    return tuple(int(s[i:i+2], 16) for i in (0, 2, 4)) + (255,)

# ---------- heads (13 rows) ----------
SHORT_DOWN = [
    "....oooooooo....",
    "..oHHhhhhhhhdo..",
    ".ohHHhhhhhhhhdo.",
    ".ohHhhhhhhhhhdo.",
    ".ohhhhhhhhhhhdo.",
    ".odhhhhhhhhhhdo.",
    ".odhssshhssshdo.",
    ".odsssssssssSdo.",
    ".osseSssssseSSo.",
    ".osseSssssseSSo.",
    "..osssssssssSo..",
    "...oSsssssSSo...",
    "....oooooooo....",
]
SHORT_UP = [
    "....oooooooo....",
    "..oHHhhhhhhhdo..",
    ".ohHHhhhhhhhhdo.",
    ".ohHhhhhhhhhhdo.",
    ".ohhhhhhhhhhhdo.",
    ".ohhhhhhhhhhhdo.",
    ".odhhhhhhhhhhdo.",
    ".odhhhhhhhhhhdo.",
    ".oddhhhhhhhhddo.",
    ".oddhhhhhhhhddo.",
    "..oddhhhhhhddo..",
    "...osddddddso...",
    "....oooooooo....",
]
SHORT_SIDE = [
    ".....oooooooo...",
    "...oHHhhhhhhdo..",
    "..oHHhhhhhhhhdo.",
    ".ohHhhhhhhhhhdo.",
    ".ohhhhhhhhhhhdo.",
    ".ohhhhhhhhhhhdo.",
    ".ohssshhhhhhhdo.",
    ".ossssshhhhhhdo.",
    ".osesssSshhhhdo.",
    ".osesssSShhhhdo.",
    "..osssssSSddo...",
    "...osssSSddo....",
    "....ooooooo.....",
]
CAP_DOWN_TOP = [
    "....oooooooo....",
    "..oMMmmmmmmmmo..",
    ".oMMmmwwwwmmmmo.",
    ".oMmmmwwwwmmmbo.",
    ".ommmmmmmmmmmbo.",
    ".obbbbbbbbbbbbo.",
    ".odhssssssssdo..",
]
CAP_UP_TOP = [
    "....oooooooo....",
    "..oMMmmmmmmmmo..",
    ".oMMmmmmmmmmmmo.",
    ".oMmmmmmmmmmmbo.",
    ".ommmmmmmmmmmbo.",
    ".obbbbwwwwbbbbo.",
    ".odhhhhhhhhhhdo.",
]
CAP_SIDE_TOP = [
    ".....oooooooo...",
    "...oMMmmmmmmmo..",
    "..oMMmmmwwwmmmo.",
    ".oMmmmmmwwwmmbo.",
    ".ommmmmmmmmmmbo.",
    "obbbbbbmmmmmbdo.",
    ".ohssshhhhhhhdo.",
]

def cap(base, top):
    return top + base[len(top):]

# ---------- bodies (9 rows: 13..21) ----------
BODY_DOWN = {
 'stand': [
    "...occcccccco...",
    "..oCcccccccCo...",
    "..oCcccccccCo...",
    "..ossccccccsso..",
    "...oppppppppo...",
    "...oppPooPppo...",
    "...okkkookkko...",
    "....ooo..ooo....",
 ],
 'stepA': [
    "...occcccccco...",
    "..oCcccccccCo...",
    "..oCcccccccCo...",
    "..ossccccccsso..",
    "...oppppppppo...",
    "...oppPookkko...",
    "...okkko.ooo....",
    "....ooo.........",
 ],
}
BODY_SIDE = {
 'stand': [
    "....occcccco....",
    "...occcccccco...",
    "...occCCcccco...",
    "...occsscccco...",
    "....opppppo.....",
    "....oppPpo......",
    "...okkkkko......",
    "....oooooo......",
 ],
 'stepA': [
    "....occcccco....",
    "...occcccccco...",
    "...oCCcccccco...",
    "...ossccccCCo...",
    "....opppppo.....",
    "...oppPoPpo.....",
    "..okkko.okko....",
    "...ooo...oo.....",
 ],
 'stepB': [
    "....occcccco....",
    "...occcccccco...",
    "...occccccCCo...",
    "...oCCccccsso...",
    "....opppppo.....",
    "....oPpoppPo....",
    "....okko.okkko..",
    ".....oo...ooo...",
 ],
}

def fix(rows):
    out = []
    for r in rows:
        r = (r + '.' * W)[:W]
        out.append(r)
    return out

def mirror(rows):
    return [r[::-1] for r in rows]

def longify(head, body, side=False):
    """long hair: extend hair down the sides of the face/shoulders"""
    head = [list(r) for r in head]
    body = [list(r) for r in body]
    if not side:
        for i in range(7, 13):
            head[i][0] = 'o'; head[i][1] = 'h'; head[i][2] = 'd' if i > 9 else 'h'
            head[i][15] = 'o'; head[i][14] = 'd'; head[i][13] = 'd'
        for i in range(0, 2):
            body[i][1] = 'o'; body[i][2] = 'd'; body[i][13] = 'd'; body[i][14] = 'o'
    else:
        for i in range(6, 13):
            for c in range(8, 14):
                if head[i][c] in 'sSo.' and c >= 9:
                    head[i][c] = 'h' if c < 12 else 'd'
            head[i][14] = 'o'
        head[12] = list("....oooooddo....")
        body[0] = list("....occccddo....")
        body[1] = list("...occcccddo....")
        body[2] = list((''.join(body[2])[:11] + "o....")[:16])
    return [''.join(r) for r in head], [''.join(r) for r in body]

def frames_for(style):
    """returns dict dir -> list of 4 frames (stand, stepA, stand, stepB), each 21 rows"""
    if style == 'cap':
        hd, hu, hs = cap(SHORT_DOWN, CAP_DOWN_TOP), cap(SHORT_UP, CAP_UP_TOP), cap(SHORT_SIDE, CAP_SIDE_TOP)
    else:
        hd, hu, hs = SHORT_DOWN, SHORT_UP, SHORT_SIDE
    bd_st, bd_a = BODY_DOWN['stand'], BODY_DOWN['stepA']
    bd_b = mirror(bd_a)
    bs_st, bs_a, bs_b = BODY_SIDE['stand'], BODY_SIDE['stepA'], BODY_SIDE['stepB']
    res = {}
    def mk(head, body):
        if style == 'long':
            head, body = longify(head, body, side=head is hs)
        return fix(head + body)
    def mks(head, body):
        h2, b2 = (longify(head, body, side=True) if style == 'long' else (head, body))
        return fix(h2 + b2)
    res['down'] = [mk(hd, bd_st), mk(hd, bd_a), mk(hd, bd_st), mk(hd, bd_b)]
    res['up'] = [mk(hu, bd_st), mk(hu, bd_a), mk(hu, bd_st), mk(hu, bd_b)]
    left = [mks(hs, bs_st), mks(hs, bs_a), mks(hs, bs_st), mks(hs, bs_b)]
    res['left'] = left
    res['right'] = [mirror(f) for f in left]
    return res

SKIN = [('#f8d0a0', '#d8a070'), ('#d8a070', '#a87048')]

def palette(v):
    hair, hairL, hairD = v['hair']
    shirt, shirtD = v['shirt']
    pants, pantsD = v['pants']
    skin, skinD = SKIN[v.get('skin', 0)]
    p = {
        'o': '#383040', 'e': '#282028', 'w': '#f8f8f8',
        's': skin, 'S': skinD,
        'h': hair, 'H': hairL, 'd': hairD,
        'c': shirt, 'C': shirtD, 'p': pants, 'P': pantsD,
        'k': '#585060',
    }
    if 'cap' in v:
        m, M, b = v['cap']
        p.update({'m': m, 'M': M, 'b': b})
    return {k: hx(c) for k, c in p.items()}

def draw(img, rows, ox, oy, pal):
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == '.':
                continue
            img.putpixel((ox + x, oy + y), pal[ch])

VARIANTS = [
    dict(name='v1', style='cap', cap=('#e05040', '#f89078', '#a02830'), hair=('#584038', '#806050', '#382820'), shirt=('#4878d0', '#3050a0'), pants=('#405070', '#283048')),
    dict(name='v2', style='short', hair=('#a86838', '#d09058', '#704020'), shirt=('#58a858', '#3c7c3c'), pants=('#504858', '#383040')),
    dict(name='v3', style='long', hair=('#f0c040', '#f8e080', '#c08820'), shirt=('#e86890', '#b84868'), pants=('#4868b0', '#304888')),
    dict(name='v4', style='short', hair=('#383840', '#585868', '#202028'), shirt=('#e8e8f0', '#b0b0c0'), pants=('#485060', '#303848'), skin=1),
    dict(name='v5', style='cap', cap=('#3870d0', '#68a0f0', '#204890'), hair=('#202028', '#404048', '#101018'), shirt=('#f08838', '#c06020'), pants=('#505868', '#383c48'), skin=1),
    dict(name='v6', style='long', hair=('#8c4830', '#b86848', '#5c2818'), shirt=('#38a0a8', '#287880'), pants=('#504858', '#383040')),
    dict(name='v7', style='short', hair=('#c8c8d0', '#f0f0f8', '#909098'), shirt=('#8858b8', '#603888'), pants=('#585060', '#403848')),
    dict(name='v8', style='long', hair=('#302838', '#504860', '#181020'), shirt=('#f0d048', '#c0a020'), pants=('#c84848', '#902828'), skin=1),
]
DIRS = ['down', 'up', 'left', 'right']

def build_sheet(v):
    fr = frames_for(v['style'])
    pal = palette(v)
    img = Image.new('RGBA', (W * 4, H * 4), (0, 0, 0, 0))
    for di, d in enumerate(DIRS):
        for fi, f in enumerate(fr[d]):
            bob = 0 if fi % 2 == 0 else -1
            draw(img, f, fi * W, di * H + 1 + bob, pal)
    return img

# ---------- desk + PC (32x30) and chair ----------
def rect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            img.putpixel((x, y), hx(c))

def desk_pc():
    img = Image.new('RGBA', (32, 30), (0, 0, 0, 0))
    O = '#503020'
    # desk body
    rect(img, 0, 12, 31, 29, O)
    rect(img, 1, 13, 30, 19, '#f0c078')
    rect(img, 1, 13, 30, 13, '#f8dca0')
    rect(img, 1, 20, 30, 20, '#985828')
    rect(img, 1, 21, 30, 28, '#c88848')
    rect(img, 1, 27, 30, 28, '#a86830')
    rect(img, 15, 21, 16, 28, '#985828')
    rect(img, 6, 23, 9, 23, '#f0c078'); rect(img, 22, 23, 25, 23, '#f0c078')
    # monitor (beige CRT)
    M = '#383040'
    rect(img, 7, 0, 24, 13, M)
    rect(img, 8, 1, 23, 12, '#e8e0c8')
    rect(img, 22, 1, 23, 12, '#c0b498')
    rect(img, 8, 11, 23, 12, '#c0b498')
    rect(img, 8, 1, 21, 1, '#f8f4e8')
    rect(img, 10, 3, 21, 10, M)
    rect(img, 11, 4, 20, 9, '#3870c8')
    rect(img, 11, 4, 12, 5, '#a8d8f8'); rect(img, 13, 4, 13, 4, '#a8d8f8')
    rect(img, 13, 6, 18, 6, '#78b0f0'); rect(img, 13, 8, 16, 8, '#78b0f0')
    rect(img, 19, 11, 20, 11, '#58c058')  # power led
    rect(img, 12, 13, 19, 14, M); rect(img, 13, 13, 18, 13, '#c0b498')
    # keyboard
    rect(img, 9, 15, 22, 18, M)
    rect(img, 10, 16, 21, 17, '#e8e0c8')
    for x in range(11, 21, 2):
        img.putpixel((x, 16), hx('#a89c80'))
    rect(img, 12, 17, 19, 17, '#c0b498')
    # mug
    rect(img, 25, 13, 28, 17, M); rect(img, 26, 14, 27, 16, '#f8f8f8'); rect(img, 26, 14, 27, 14, '#e05040')
    # papers
    rect(img, 2, 14, 6, 18, '#a8a0a8'); rect(img, 3, 15, 6, 18, '#f8f8f8'); rect(img, 3, 16, 5, 16, '#b0b0c0')
    return img

def chair():
    img = Image.new('RGBA', (14, 14), (0, 0, 0, 0))
    O = '#303048'
    rect(img, 1, 0, 12, 9, O)
    rect(img, 0, 2, 13, 9, O)
    rect(img, 2, 1, 11, 8, '#7868b8')
    rect(img, 1, 3, 12, 8, '#7868b8')
    rect(img, 2, 1, 4, 3, '#a898e0')
    rect(img, 1, 7, 12, 8, '#584890')
    rect(img, 5, 10, 8, 11, O); rect(img, 2, 12, 11, 13, O); rect(img, 3, 12, 10, 12, '#686878')
    return img

if __name__ == '__main__':
    sheets = []
    for v in VARIANTS:
        s = build_sheet(v)
        s.save(os.path.join(OUT, f"npc_{v['name']}.png"))
        sheets.append(s)
    d = desk_pc(); d.save(os.path.join(OUT, 'desk_pc.png'))
    c = chair(); c.save(os.path.join(OUT, 'chair.png'))
    # preview: all sheets side by side + desk, scaled 5x on grass
    pw = W * 4 * len(sheets) + 8 * len(sheets) + 48
    prev = Image.new('RGBA', (pw, H * 4 + 40), hx('#88c868'))
    x = 4
    for s in sheets:
        prev.alpha_composite(s, (x, 4)); x += W * 4 + 8
    prev.alpha_composite(d, (x, 4)); prev.alpha_composite(c, (x + 9, 40))
    prev = prev.resize((prev.width * 4, prev.height * 4), Image.NEAREST)
    prev.save(os.path.join(OUT, 'preview.png'))
    print('ok')
