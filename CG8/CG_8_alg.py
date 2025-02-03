class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def check_convex(arr: list[point]):
    # Если не многоугольник - false
    if len(arr) < 3:
        return 1
    # Цикл проверки скалярных произведений отрезков, выходящих из каждой точки
    # Если скалярные произведения для всех точек имеют один знак, то многоугольник выпуклый
    flag = 0
    for i in range(len(arr)):
        ab = point(arr[i].x - arr[i - 1].x, arr[i].y - arr[i - 1].y)
        bc = point(arr[(i + 1) % len(arr)].x - arr[i].x, arr[(i + 1) % len(arr)].y - arr[i].y)
        product = ab.x * bc.y - ab.y * bc.x
        # Заносим первое произведение в флаг, по сути от него нам нужен только знак
        if flag == 0:
            flag = product
        else:
            # Если произведение первого скалярного на текущее скалярное меньше нуля, то у них разные знаки
            if flag * product < 0:
                return 1
    return 0

'''
Функция определения координат внутренней нормали к стороне p1p2
Точка p3 нужна для определения именно внутренней нормали, а не внешней'''
def inside_normal(p1: point, p2: point, p3: point):
    # Сначала вычисляем координаты вектора p1p2
    ab = point(p2.x - p1.x, p2.y - p1.y)
    normal = point(None, None)
    # Если отрезок вертикальный
    if ab.x == 0:
        normal.x = 1
        normal.y = 0
    # Если отрезок горизонтальный
    elif ab.y == 0:
        normal.x = 0
        normal.y = 1
    else:
        normal.x = 1
        normal.y = -(ab.x / ab.y)
    # Теперь проверим нормаль на внутренность
    # ac - отрезок p1p3
    ac = point(p3.x - p2.x, p3.y - p2.y)
    # Скалярное произведение нормали и p1p3
    # Если оно меньше нуля, то нормаль внешняя, нужно ее отразить
    product = ac.x * normal.x + ac.y * normal.y
    if product < 0:
        normal.x *= -1
        normal.y *= -1
    return normal


def cut(p1: point, p2: point, cutter: list[point]):
    if check_convex(cutter) == 1:
        return None, None
    # Параметрическая форма записи уравнения отрезка
    t_start = 0
    t_end = 1
    # Вектор отрезка
    D = point(p2.x - p1.x, p2.y - p1.y)
    for i in range(len(cutter)):
        # Вычисляем внутреннюю нормаль к очередной стороне отсекателя
        normal = inside_normal(cutter[i], cutter[(i + 1) % len(cutter)], cutter[(i + 2) % len(cutter)])
        # Вектор, соединяющий точку отрезка и произвольную точку на отсекателе
        W = point(p1.x - cutter[i].x, p1.y - cutter[i].y)
        # Скалярное произведение вектора внутренней нормали на вектор отрезка
        D_scalar = normal.x * D.x + normal.y * D.y
        # Скалярное произведение вектора внутренней нормали на вектор соединяющий точку отрезка с произвольной точкой отсекателя
        W_scalar = normal.x * W.x + normal.y * W.y
        # D_scalar == 0 если P1 == P2, тогда считаем точкой, проверяем вектор от стороны отсекателя к точке
        # D_scalar == 0 если P1P2 перпендикулярен внутренней нормали. Проверяем W_scalar, если он меньше 0 то отрезок невидим
        if D_scalar == 0:
            # Невидимый отрезок
            if W_scalar < 0:
                return None, None
            else:
                continue
        # Если отрезок не параллеллен границе и не точка, можем найти точки пересечения с ребром отсекателя
        t = -1.0 * W_scalar / D_scalar
        if D_scalar > 0:
            # Невидимый отрезок
            if t > 1:
                return None, None
            else:
                t_start = max(t, t_start)
                continue
        if D_scalar < 0:
            # Невидимый отрезок
            if t < 0:
                return None, None
            else:
                t_end = min(t, t_end)
    if t_end < t_start:
        return None, None
    p3 = point(round(p1.x + (p2.x - p1.x) * t_start), round(p1.y + (p2.y - p1.y) * t_start))
    p4 = point(round(p1.x + (p2.x - p1.x) * t_end), round(p1.y + (p2.y - p1.y) * t_end))
    return p3, p4

