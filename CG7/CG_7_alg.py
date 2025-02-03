class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


'''
Функция определения видимости отрезка и поиска кодов
его концов
'''
def check_function(p1: point, p2: point, xl, xr, ylow, yup):
    t1 = []
    t2 = []
    t1.append(int(p1.x < xl))
    t1.append(int(p1.x > xr))
    t1.append(int(p1.y < ylow))
    t1.append(int(p1.y > yup))

    t2.append(int(p2.x < xl))
    t2.append(int(p2.x > xr))
    t2.append(int(p2.y < ylow))
    t2.append(int(p2.y > yup))

    s1 = sum(t1)
    s2 = sum(t2)
    p = 0
    for i in range(4):
        p += t1[i] * t2[i]
    # Полная видимость
    if s1 == 0 and s2 == 0:
        return t1, t2, 1
    # Полная невидимость
    if p != 0:
        return t1, t2, -1
    # Частичная видимость
    return t1, t2, 0


'''
x0, y0, x1, y1 - координаты концов отсекаемого отрезка
xl, xr - левая и правая граница прямоугольного отсекателя
yup, ylow - верхняя и нижняя граница отсекателя
'''
def cut(p0: point, p1:point, xl: int, xr: int, ylow: int, yup: int):
    if xr <= xl or yup <= ylow:
        return None, None
    fl = 1
    m = 0
    # Если отрезок вертикальный, fl = -1
    # Если отрезок горизонтальный, fl = 0
    # Иначе fl = 1
    if p1.y == p0.y:
        fl = 0
    elif p0.x == p1.x:
        fl = -1
    else:
        m = ((p1.y - p0.y) * 1.0) / (p1.x - p0.x)
    arr = [xl, xr, ylow, yup]
    for i in range(4):
        t0, t1, wid = check_function(p0, p1, xl, xr, ylow, yup)
        # Полная видимость - отображаем весь отрезок
        if wid == 1:
            return p0, p1
        # Полная невидимость - не отображаем отрезок
        elif wid == -1:
            return None, None
        if t0[i] == t1[i]:
            continue
        if t0[i] == 0:
            p0, p1 = p1, p0
        if fl != -1:
            if i < 2:
                p0.y = round(m * (arr[i] - p0.x) + p0.y)
                p0.x = arr[i]
            else:
                p0.x = round((arr[i] - p0.y) * 1.0 / m + p0.x)
                p0.y = arr[i]
        else:
            p0.y = arr[i]
    return p0, p1
