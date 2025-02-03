import numpy as np
def bresenham_integers(data):
    arr = []
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
        if swap == 0:
            x += sx
        else:
            y += sy
        e += dob_dy
    return arr
