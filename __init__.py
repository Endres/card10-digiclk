import display
import leds
import utime

def ceilDiv(a, b):
    return (a + (b - 1)) // b

def tipHeight(w):
    return ceilDiv(w, 2) - 1

def drawTip(d, x, y, w, c, invert = False, swapAxes = False):
    h = tipHeight(w)
    for dy in range(h):
        for dx in range(dy + 1, w - 1 - dy):
            px = x + dx
            py = y + dy if not invert else y + h - 1 - dy
            if swapAxes:
                px, py = py, px
            d.pixel(px, py, col = c)

def drawSeg(d, x, y, w, h, c, swapAxes = False):
    tip_h = tipHeight(w)
    body_h = h - 2 * tip_h

    drawTip(d, x, y, w, c, invert = True, swapAxes = swapAxes)

    px1, px2 = x, x + w
    py1, py2 = y + tip_h, y + tip_h + body_h
    if swapAxes:
        px1, px2, py1, py2 = py1, py2, px1, px2
    d.rect(px1, py1, px2, py2, col = c)

    drawTip(d, x, y + tip_h + body_h, w, c, invert = False, swapAxes = swapAxes)

def drawVSeg(d, x, y, w, l, c):
    drawSeg(d, x, y, w, l, c)

def drawHSeg(d, x, y, w, l, c):
    drawSeg(d, y, x, w, l, c, swapAxes = True)

def drawGridSeg(d, x, y, w, l, c, swapAxes = False):
    sw = w - 2
    tip_h = tipHeight(sw)

    x = x * w
    y = y * w
    l = (l - 1) * w
    drawSeg(d, x + 1, y + tip_h + 3, sw, l - 3, c, swapAxes = swapAxes)

def drawGridVSeg(d, x, y, w, l, c):
    drawGridSeg(d, x, y, w, l, c)

def drawGridHSeg(d, x, y, w, l, c):
    drawGridSeg(d, y, x, w, l, c, swapAxes = True)

def drawGrid(d, x1, y1, x2, y2, w, c):
    for x in range(x1 * w, x2 * w):
        for y in range(y1 * w, y2 * w):
            if x % w == 0 or x % w == w - 1 or y % w == 0 or y % w == w - 1:
                d.pixel(x, y, col = c)

def drawGrid7Seg(d, x, y, w, segs, c):
    if segs[0]:
        drawGridHSeg(d, x, y, w, 4, c)
    if segs[1]:
        drawGridVSeg(d, x + 3, y, w, 4, c)
    if segs[2]:
        drawGridVSeg(d, x + 3, y + 3, w, 4, c)
    if segs[3]:
        drawGridHSeg(d, x, y + 6, w, 4, c)
    if segs[4]:
        drawGridVSeg(d, x, y + 3, w, 4, c)
    if segs[5]:
        drawGridVSeg(d, x, y, w, 4, c)
    if segs[6]:
        drawGridHSeg(d, x, y + 3, w, 4, c)

DIGITS = [
    (True, True, True, True, True, True, False),
    (False, True, True, False, False, False, False),
    (True, True, False, True, True, False, True),
    (True, True, True, True, False, False, True),
    (False, True, True, False, False, True, True),
    (True, False, True, True, False, True, True),
    (True, False, True, True, True, True, True),
    (True, True, True, False, False, False, False),
    (True, True, True, True, True, True, True),
    (True, True, True, True, False, True, True)
]

DISPLAY = 0
CHANGE_HOURS = 1
CHANGE_MINUTES = 2
CHANGE_SECONDS = 3
CHANGE_NAME = 4
MODE = DISPLAY
MODES = {
    DISPLAY: '---',
    CHANGE_HOURS: 'HRS',
    CHANGE_MINUTES: 'MNS',
    CHANGE_MINUTES: 'SEC',
    CHANGE_NAME: 'NAM'
}

def renderNum(d, num, blank1, blank2, x):
    if not blank1:
        drawGrid7Seg(d, x, 0, 7, DIGITS[num // 10], (255, 255, 255))
    if not blank2:
        drawGrid7Seg(d, x + 5, 0, 7, DIGITS[num % 10], (255, 255, 255))

def renderColon(d, blank):
    if not blank:
        drawGridVSeg(d, 11, 2, 7, 2, (255, 255, 255))
        drawGridVSeg(d, 11, 4, 7, 2, (255, 255, 255))

def renderText(d, text, blanks):
    bs = bytearray(text.encode())
    for i, b in enumerate(blanks):
        if b:
            bs[i:i+1] = b'_'
    d.print(MODES[MODE] + ' ' + bs.decode(), fg = (255, 255, 255), bg = None, posx = 0, posy = 7 * 8)

def render():
    with display.open() as d:
        ltime = utime.localtime()
        hours = ltime[3]
        mins = ltime[4]
        secs = ltime[5]

        d.clear()
        #drawGrid(d, 1, 0, 22, 7, 7, (255, 0, 0))

        renderNum(d, hours, False, False, 1)
        renderColon(d, secs % 2 == 1)
        renderNum(d, mins, False, False, 13)
        renderText(d, "yrlf", [])

        d.update()

try:
    while True:
        render()
except KeyboardInterrupt:
    pass
