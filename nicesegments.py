SEGMENTS = [[(6, 0, 19, 1), (7, 2, 18, 2)],
    [(21, 2), (20, 3, 21, 3), (19, 4, 21, 6), (18, 7, 20, 17), (17, 18, 19, 21),
    (19, 22)],
    [(19, 24), (17, 25, 19, 29), (16, 30, 18, 40), (15, 41, 17, 43),
    (16, 44, 17, 44), (17, 45)],
    [(3, 45, 14, 45), (2, 46, 15, 47)],
    [(2, 24), (2, 25, 4, 29), (1, 30, 3, 40), (0, 41, 2, 43), (0, 44, 1, 44),
    (0, 45)],
    [(4, 2), (4, 3, 5, 3), (4, 4, 6, 6), (3, 6, 5, 17), (2, 18, 4, 21),
    (2, 22)],
    [(4, 23, 17, 23), (6, 22, 15, 24)]]
SEGMENT_COLON = [(8, 13), (6, 14, 8, 16), (6, 17), (5, 32), (3, 33, 5, 35),
    (3, 36)]

def Seg(d, x, y, c, data):
    for coord_tuple in data:
        if len(coord_tuple) == 2:
            d.pixel(x + coord_tuple[0], y + coord_tuple[1], col = c)
        else:
            d.rect(x + coord_tuple[0], y + coord_tuple[1], \
            x + coord_tuple[2] + 1, y + coord_tuple[3] + 1, col = c)

def Grid7Seg(d, x, y, segs, c):
    for i in range(7):
        if segs[i]:
            Seg(d, x, y, c, SEGMENTS[i])

def GridColon(d, x, y, c):
    Seg(d, x, y, c, SEGMENT_COLON)
