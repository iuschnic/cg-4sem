import math

eps = 0.0001


# Функция по заданному центру и точке возвращает массив точек симметричных данной в 4 четвертях
def symmetric_four(center, point):
    ans = []
    cx, cy = center[0], center[1]
    px, py = point[0], point[1]
    dx, dy = px - cx, py - cy
    ans.append([cx + dx, cy + dy])
    ans.append([cx + dx, cy - dy])
    ans.append([cx - dx, cy + dy])
    ans.append([cx - dx, cy - dy])
    return ans


# Функция по заданному центру и точке возвращает массив точек симметричных данной в 8 частях окружности
def symmetric_eight(center, point):
    ans = symmetric_four(center, point)
    cx, cy = center[0], center[1]
    px, py = point[0], point[1]
    dx, dy = px - cx, py - cy
    # координаты точки в смежной 1/8 части
    newx = dy + cx
    newy = dx + cy
    new = symmetric_four(center, [newx, newy])
    for elem in new:
        ans.append(elem)
    return ans


def canonical_circle(data):
    arr = []
    x0 = round(data[0])
    y0 = round(data[1])
    r = round(data[2])
    x = x0
    while x < x0 + (r / math.sqrt(2)) + 1:
        y = math.sqrt(r ** 2 - (x - x0) ** 2) + y0
        ans = symmetric_eight([x0, y0], [round(x), round(y)])
        for elem in ans:
            arr.append(elem)
        x += 1
    return arr


def parametr_circle(data):
    arr = []
    x0 = round(data[0])
    y0 = round(data[1])
    r = round(data[2])
    inc_angle = 1 / r
    angle = math.pi / 2
    while angle > math.pi / 4:
        x = round(math.cos(angle) * r + x0)
        y = round(math.sin(angle) * r + y0)
        ans = symmetric_eight([x0, y0], [x, y])
        for elem in ans:
            arr.append(elem)
        angle -= inc_angle
    return arr


def bres_circle(data):
    arr = []
    x0 = round(data[0])
    y0 = round(data[1])
    r = round(data[2])

    # начинаем работу алгоритма с верхней точки окружности
    # x, y - координаты точки в осях связанных с центром окружности, далее корректируем это где нужно
    x = 0
    y = r
    # delta = (xi + 1) ^ 2 + (yi - 1) ^ 2 - R ^ 2
    # delta_start = 1 + R ^ 2 - 2 * R + 1 - R ^ 2 = 2 - 2 * R = 2 * (1 - R)
    delta = 2 * (1 - r)
    ans = symmetric_eight([x0, y0], [x0, y0 + r])
    for elem in ans:
        arr.append(elem)
    # Работаем только в верхней восьмой части (верхняя половина первой четверти)
    # Поэтому можно не добавлять третий случай в if когда меняется только y
    while x < y:
        d = 2 * delta + 2 * y - 1
        if d < 0:
            x += 1
            delta += 2 * x + 1
        else:
            x += 1
            y -= 1
            delta += 2 * (x - y + 1)
        ans = symmetric_eight([x0, y0], [x + x0, y + y0])
        for elem in ans:
            arr.append(elem)
    return arr


def central_point_circle(data):
    arr = []
    x0 = round(data[0])
    y0 = round(data[1])
    a = round(data[2])
    b = round(data[2])

    # единственное отличие от алгоритма эллипса - равенство полуосей a и b
    a_sq = a * a
    b_sq = b * b

    # начинаем строить с верхней точки эллипса, строим первую четверть
    x = 0
    y = b

    # граница инкрементации по x и по y
    border_x = a_sq / (math.sqrt(a_sq + b_sq))  # выведено из равенства производной уравнения эллипса единице
    border_y = b_sq / (math.sqrt(a_sq + b_sq))

    # начальное значение пробной функции fi = b^2 * (xi-1 + 1)^2 + a^2 * (yi-1 - 1/2)^2 - (a * b)^2
    # f0 = b^2 + a^2 * (b^2 - b + 1/4) - (a * b) ^ 2 = b^2 - a^2 * b + a^2 / 4
    f = b_sq + a_sq / 4 - a_sq * b

    for i in range(0, round(border_x)):
        ans = symmetric_four([x0, y0], [x + x0, y + y0])
        for elem in ans:
            arr.append(elem)
        if f <= 0:
            x += 1
            f += 2 * b_sq * x + b_sq
        else:
            x += 1
            y -= 1
            f += 2 * b_sq * x + b_sq
            f += - 2 * a_sq * y

    # для перехода в центральной точке меняем f
    f += -(a_sq * y + b_sq * x) + 3 * (a_sq - b_sq) / 4
    for i in range(round(border_y), -1, -1):
        ans = symmetric_four([x0, y0], [x + x0, y + y0])
        for elem in ans:
            arr.append(elem)
        if f >= 0:
            y -= 1
            f += -2 * a_sq * y + a_sq
        else:
            x += 1
            y -= 1
            f += -2 * a_sq * y + a_sq
            f += 2 * b_sq * x
    return arr


def canonical_ellypse(data):
    arr = []
    x0 = round(data[0])
    y0 = round(data[1])
    a = round(data[2])
    b = round(data[3])

    a_sq = a * a
    b_sq = b * b

    # границы инкрементации по x и по y
    border_x = a_sq / (math.sqrt(a_sq + b_sq))     # выведено из равенства производной уравнения эллипса единице
    border_y = b_sq / (math.sqrt(a_sq + b_sq))

    for i in range(0, round(border_x) + 1):
        x = i
        y = round(math.sqrt((a_sq * b_sq - b_sq * x * x) / a_sq)) + y0     # из уравнения эллипса получаем новую точку
        ans = symmetric_four([x0, y0], [x + x0, y])
        for elem in ans:
            arr.append(elem)

    for i in range(0, round(border_y) + 1):
        y = i
        x = round(math.sqrt((a_sq * b_sq - a_sq * y * y) / b_sq)) + x0     # из уравнения эллипса получаем новую точку
        ans = symmetric_four([x0, y0], [x, y + y0])
        for elem in ans:
            arr.append(elem)

    return arr


def parametr_ellypse(data):
    arr = []
    x0 = round(data[0])
    y0 = round(data[1])
    a = round(data[2])
    b = round(data[3])

    inc_angle = 1 / a if a > b else 1 / b
    angle = math.pi / 2
    # Работаем только в верхней правой четверти
    while angle > 0:
        x = round(math.cos(angle) * a + x0)
        y = round(math.sin(angle) * b + y0)
        ans = symmetric_four([x0, y0], [x, y])
        for elem in ans:
            arr.append(elem)
        angle -= inc_angle
    return arr


def bres_ellypse(data):
    arr = []
    x0 = round(data[0])
    y0 = round(data[1])
    a = round(data[2])
    b = round(data[3])
    a_sq = a * a
    b_sq = b * b

    # начинаем работу алгоритма с верхней точки окружности
    # x, y - координаты точки в осях связанных с центром окружности, далее корректируем это где нужно
    x = 0
    y = b
    # delta = b ^ 2 * (xi + 1) ^ 2 + a ^ 2 * (yi - 1) ^ 2 - (a * b) ^ 2
    # delta_start = b ^ 2 + (a * b) ^ 2 - 2 * b * a ^ 2 + a ^ 2 - (a * b) ^ 2 = a ^ 2 + b ^ 2 - 2 * b * a ^ 2
    delta = a_sq + b_sq - 2 * b * a_sq
    ans = symmetric_four([x0, y0], [x0, y0 + b])
    for elem in ans:
        arr.append(elem)
    # Работаем только в верхней правой четверти
    while y >= 0:
        # Точно диагональный шаг
        if delta == 0:
            x += 1
            y -= 1
            delta += (2 * x + 1) * b_sq + (1 - 2 * y) * a_sq
        # Горизонтальный или диагональный
        elif delta < 0:
            d = 2 * delta + (2 * y - 1) * a_sq
            # Горизонтальный шаг
            if d <= 0:
                x += 1
                delta += (2 * x + 1) * b_sq
            # Диагональный шаг
            else:
                x += 1
                y -= 1
                delta += (2 * x + 1) * b_sq + (1 - 2 * y) * a_sq
            #delta += (2 * x + 1) * b_sq
        # Вертикальный или диагональный
        else:
            d = 2 * delta + (- 2 * x - 1) * b_sq
            # Диагональный
            if d <= 0:
                x += 1
                y -= 1
                delta += (2 * x + 1) * b_sq + (1 - 2 * y) * a_sq
            # Вертикальный
            else:
                y -= 1
                delta += (-2 * y + 1) * a_sq

        ans = symmetric_four([x0, y0], [x + x0, y + y0])
        for elem in ans:
            arr.append(elem)
    return arr

def central_point_ellypse(data):
    arr = []
    x0 = round(data[0])
    y0 = round(data[1])
    a = round(data[2])
    b = round(data[3])

    a_sq = a * a
    b_sq = b * b

    # начинаем строить с верхней точки эллипса, строим первую четверть
    x = 0
    y = b

    # граница инкрементации по x и по y
    border_x = a_sq / (math.sqrt(a_sq + b_sq))  # выведено из равенства производной уравнения эллипса единице
    border_y = b_sq / (math.sqrt(a_sq + b_sq))

    # начальное значение пробной функции fi = b^2 * (xi-1 + 1)^2 + a^2 * (yi-1 - 1/2)^2 - (a * b)^2
    # f0 = b^2 + a^2 * (b^2 - b + 1/4) - (a * b) ^ 2 = b^2 - a^2 * b + a^2 / 4
    f = b_sq + a_sq / 4 - a_sq * b

    for i in range(0, round(border_x)):
        ans = symmetric_four([x0, y0], [x + x0, y + y0])
        for elem in ans:
            arr.append(elem)
        if f <= 0:
            x += 1
            f += 2 * b_sq * x + b_sq
        else:
            x += 1
            y -= 1
            f += 2 * b_sq * x + b_sq
            f += - 2 * a_sq * y

    # для перехода в центральной точке меняем f
    f += -(a_sq * y + b_sq * x) + 3 * (a_sq - b_sq) / 4
    for i in range(round(border_y), -1, -1):
        ans = symmetric_four([x0, y0], [x + x0, y + y0])
        for elem in ans:
            arr.append(elem)
        if f >= 0:
            y -= 1
            f += -2 * a_sq * y + a_sq
        else:
            x += 1
            y -= 1
            f += -2 * a_sq * y + a_sq
            f += 2 * b_sq * x
    return arr


