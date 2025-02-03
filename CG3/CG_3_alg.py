import numpy as np
eps = 0.0001

def cda(data, flag):
    arr = []
    steps = 1
    if not data:
        return None
    x1 = data[0]
    y1 = data[1]
    x2 = data[2]
    y2 = data[3]
    dx = x2 - x1
    dy = y2 - y1
    x = round(x1)
    y = round(y1)

    if int(abs(dx)) == 0 and int(abs(dy)) == 0:
        arr.append([round(x), round(y)])
        steps = 1
        return arr, steps

    swap = 0
    if abs(dx) >= abs(dy):
        swap = 1
        l = abs(dx)
    else:
        swap = 0
        l = abs(dy)
    dx = dx / l
    dy = dy / l
    for i in range(0, int(l) + 1):
        arr.append([round(x), round(y)])
        if flag == 1:
            if swap and round(abs(y + dy)) > round(abs(y)):
                steps += 1
            elif not swap and round(abs(x + dx)) > round(abs(x)):
                steps += 1
        x += dx
        y += dy
    return arr, steps

def bresenham_ord(data):
    arr = []
    steps = 1
    if not data:
        return None
    x1 = data[0]
    y1 = data[1]
    x2 = data[2]
    y2 = data[3]
    dx = x2 - x1
    dy = y2 - y1
    x = round(x1)
    y = round(y1)

    sx, sy = int(np.sign(dx)), int(np.sign(dy))

    dx = abs(dx)
    dy = abs(dy)

    if int(dx) == 0 and int(dy) == 0:
        arr.append([x, y])
        steps = 1
        return arr, steps

    swap = 0
    if dx < dy:
        swap = 1
        dx, dy = dy, dx
    m = dy / dx
    e = m - 0.5
    i = 0
    while i < dx:
        arr.append([x, y])
        if e >= 0:
            if swap == 0:
                y += sy
            else:
                x += sx
            e -= 1
            steps += 1
        if swap == 0:
            x += sx
        else:
            y += sy
        e += m
        i += 1
    return arr, steps


def bresenham_integers(data):
    arr = []
    steps = 1
    if not data:
        return None
    x1 = data[0]
    y1 = data[1]
    x2 = data[2]
    y2 = data[3]
    dx = x2 - x1
    dy = y2 - y1
    x = round(x1)
    y = round(y1)

    sx, sy = int(np.sign(dx)), int(np.sign(dy))

    dx = abs(dx)
    dy = abs(dy)

    if int(dx) == 0 and int(dy) == 0:
        arr.append([x, y])
        steps = 1
        return arr, steps

    swap = 0
    if dx < dy:
        swap = 1
        dx, dy = dy, dx

    e = 2 * dy - dx
    dob_dx = 2 * dx
    dob_dy = 2 * dy
    for i in range(0, int(dx) + 1):
        arr.append([x, y])
        if e >= 0:
            if swap == 0:
                y += sy
            else:
                x += sx
            e -= dob_dx
            steps += 1
        if swap == 0:
            x += sx
        else:
            y += sy
        e += dob_dy
    return arr, steps


def bresenham_del_steps(data):
    arr = []
    steps = 1
    if not data:
        return None
    x1 = data[0]
    y1 = data[1]
    x2 = data[2]
    y2 = data[3]
    dx = x2 - x1
    dy = y2 - y1

    sx, sy = int(np.sign(dx)), int(np.sign(dy))

    dx = abs(dx)
    dy = abs(dy)
    swap = 0
    if dx < dy:
        swap = 1
        dx, dy = dy, dx
    Imax = 1
    x = round(x1)
    y = round(y1)
    if int(dx) == 0 and int(dy) == 0:
        arr.append([x, y])
        steps = 1
        return arr, steps
    m = Imax * dy / dx
    w = Imax - m
    e = Imax / 2
    arr.append([x, y, m / 2])
    i = 0
    while i < dx + 1:
        if e <= w:
            if swap == 1:
                y += sy
            else:
                x += sx
            e += m
        else:
            x += sx
            y += sy
            e -= w
            steps += 1
        arr.append([x, y, Imax - e])
        i += 1
    return arr, steps


def wu_alg(data):
    arr = []
    steps = 1
    if not data:
        return None
    x1 = data[0]
    y1 = data[1]
    x2 = data[2]
    y2 = data[3]
    dx = x2 - x1
    dy = y2 - y1

    sx, sy = int(np.sign(dx)), int(np.sign(dy))

    dx = abs(dx)
    dy = abs(dy)
    swap = 0
    if dx < dy:
        swap = 1
        dx, dy = dy, dx
        sx, sy = sy, sx
    if swap == 1:
        x = round(y1)
        y = round(x1)
    else:
        x = round(x1)
        y = round(y1)
    if int(dx) == 0 and int(dy) == 0:
        arr.append([x, y])
        steps = 1
        return arr, steps
    m = dy / dx
    i = 0
    while i < dx + 1:
        tmp_y = round(y)
        tmp_x = round(x)
        if swap == 1:
            arr.append([tmp_y, tmp_x, 1 - (y - tmp_y)])
            arr.append([tmp_y + 1, tmp_x, y - tmp_y])
        else:
            arr.append([tmp_x, tmp_y, 1 - (y - tmp_y)])
            arr.append([tmp_x, tmp_y + 1, y - tmp_y])
        if round(y + m) > round(y):
            steps += 1
        x += sx
        y += sy * m
        i += 1
    return arr, steps
