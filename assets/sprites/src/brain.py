from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
FW, FH = 80, 72

def hx(s):
    s = s.lstrip('#')
    return tuple(int(s[i:i+2], 16) for i in (0, 2, 4)) + (255,)

def rect(img, ox, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            img.putpixel((ox + x, y), hx(c))

O = '#303040'
BODY, BODY_L, BODY_D = '#c8d0e0', '#e8f0f8', '#98a0b8'
RACK, RACK_L, RACK_D = '#6878a8', '#8898c8', '#485880'
STRIPE, STRIPE_L = '#d84848', '#f08080'

def rack(img, ox, x0, frame, flip):
    x1 = x0 + 19
    rect(img, ox, x0, 8, x1, 71, O)
    rect(img, ox, x0 + 1, 9, x1 - 1, 70, RACK)
    rect(img, ox, x0 + 1, 9, x1 - 1, 10, RACK_L)
    rect(img, ox, (x1 - 2) if not flip else (x0 + 1), 11, (x1 - 1) if not flip else (x0 + 2), 70, RACK_D)
    # 4 drive bays with blinking leds
    leds = ['#58e070', '#f8d040', '#58e070', '#f05050']
    for i in range(4):
        y = 14 + i * 12
        rect(img, ox, x0 + 3, y, x1 - 4, y + 8, O)
        rect(img, ox, x0 + 4, y + 1, x1 - 5, y + 7, RACK_D)
        for j in range(3):
            rect(img, ox, x0 + 6, y + 2 + j * 2, x1 - 8, y + 2 + j * 2, '#384068')
        on = (i + frame + (1 if flip else 0)) % 2 == 0
        c = leds[(i + (2 if flip else 0)) % 4] if on else '#283048'
        rect(img, ox, x1 - 7, y + 3, x1 - 6, y + 4, c)
    # feet
    rect(img, ox, x0, 66, x1, 71, O)
    rect(img, ox, x0 + 1, 66, x1 - 1, 69, RACK_D)

def brain(img, ox, frame):
    rack(img, ox, 0, frame, False)
    rack(img, ox, 60, frame, True)
    # central terminal: monitor housing
    rect(img, ox, 16, 0, 63, 40, O)
    rect(img, ox, 17, 1, 62, 39, BODY)
    rect(img, ox, 17, 1, 62, 2, BODY_L)
    rect(img, ox, 17, 1, 18, 39, BODY_L)
    rect(img, ox, 61, 3, 62, 39, BODY_D)
    rect(img, ox, 17, 36, 62, 39, BODY_D)
    # screen bezel + screen
    rect(img, ox, 21, 4, 58, 33, O)
    rect(img, ox, 22, 5, 57, 32, '#203028')
    rect(img, ox, 23, 6, 25, 7, '#406850')
    # red stripe on the top of the housing
    rect(img, ox, 30, 1, 49, 2, STRIPE)
    rect(img, ox, 30, 1, 49, 1, STRIPE_L)
    # console ledge with keyboard
    rect(img, ox, 14, 40, 65, 50, O)
    rect(img, ox, 15, 41, 64, 49, BODY)
    rect(img, ox, 15, 41, 64, 42, BODY_L)
    rect(img, ox, 15, 48, 64, 49, BODY_D)
    rect(img, ox, 20, 43, 47, 47, O)
    rect(img, ox, 21, 44, 46, 46, '#f0f0f8')
    for x in range(22, 46, 3):
        rect(img, ox, x, 44, x, 44, '#a8b0c0')
        rect(img, ox, x + 1, 46, x + 1, 46, '#a8b0c0')
    # chain sockets (6), first and third lit
    lit = {0, 2}
    for i in range(6):
        x = 50 + (i % 3) * 4
        y = 43 + (i // 3) * 3
        c = ('#58e070' if frame == 0 else '#90f8a0') if i in lit else '#505868'
        rect(img, ox, x, y, x + 2, y + 1, c)
    # base cabinet
    rect(img, ox, 18, 50, 61, 71, O)
    rect(img, ox, 19, 51, 60, 70, BODY)
    rect(img, ox, 19, 51, 60, 52, BODY_D)
    rect(img, ox, 19, 66, 60, 70, BODY_D)
    rect(img, ox, 58, 53, 60, 65, BODY_D)
    # red stripe band
    rect(img, ox, 19, 56, 60, 59, STRIPE)
    rect(img, ox, 19, 56, 60, 56, STRIPE_L)
    # disk slots
    rect(img, ox, 24, 61, 37, 63, O); rect(img, ox, 25, 62, 36, 62, '#606878')
    rect(img, ox, 42, 61, 55, 63, O); rect(img, ox, 43, 62, 54, 62, '#606878')
    rect(img, ox, 52, 53, 53, 54, '#58e070' if frame == 0 else '#305838')

img = Image.new('RGBA', (FW * 2, FH), (0, 0, 0, 0))
brain(img, 0, 0)
brain(img, FW, 1)
img.save(os.path.join(OUT, 'brain.png'))
img.resize((img.width * 4, img.height * 4), Image.NEAREST).save(os.path.join(OUT, 'brain_preview.png'))
print('ok')
