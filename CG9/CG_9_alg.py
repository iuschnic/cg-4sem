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


def scalar_product(fir: point, sec: point):
    return (fir.x * sec.x) + (fir.y * sec.y)


# p - точка, normal - внутренняя нормаль ребра
# clip_fir, clip_sec - вершины ребра
def check_visible(p: point, normal: point, clip_fir: point, clip_sec: point):
    #вычислим вектор fir-p
    vec = point(clip_fir.x - p.x, clip_fir.y - p.y)
    # вычислим скалярное произведение
    if scalar_product(normal, vec) <= 0:
        return True
    return False


# line_fir, line_sec - вершины отрезка
# clip_fir, clip_sec - вершины отсекателя
# normal - внутренняя нормаль отсекателя
# Проверяется пересечение отрезка и прямой, включающей отсекатель
def check_intersection(line_fir: point, line_sec: point, clip_fir: point, clip_sec: point, normal: point):
    f1 = check_visible(line_fir, normal, clip_fir, clip_sec)
    f2 = check_visible(line_sec, normal, clip_fir, clip_sec)
    if (f1 and not f2) or (f2 and not f1):
        return True
    return False


# DONE
# Функция поулчает точку пересечения ОТРЕЗКА line с ПРЯМОЙ clip
# При этом уже гарантируется что они пересекаются
def get_intersection(line_fir: point, line_sec: point, clip_fir: point, clip_sec: point):
    # матрица коэффициентов уравнений прямых
    coef = [[line_sec.x - line_fir.x, clip_fir.x - clip_sec.x],
            [line_sec.y - line_fir.y, clip_fir.y - clip_sec.y]]
    # матрица правых частей уравнений
    right = [[clip_fir.x - line_fir.x], [clip_fir.y - line_fir.y]]
    # вычислим обратную матрицу coef
    d = 1.0 * (coef[0][0] * coef[1][1] - coef[1][0] * coef[0][1])     # дискриминант
    inv = [[coef[1][1] / d, -coef[0][1] / d],
           [-coef[1][0] / d, coef[0][0] / d]]
    p = inv[0][0] * right[0][0] + inv[0][1] * right[1][0]     # элемент [0, 0] матрицы произведения inv и right
    x = line_fir.x + (line_sec.x - line_fir.x) * p
    y = line_fir.y + (line_sec.y - line_fir.y) * p
    return point(round(x), round(y))


def sutherland_hodgman(cutter: list[point], obj: list[point]):
    if check_convex(cutter) == 1:
        return None
    S = point(None, None)
    for i in range(len(cutter)):
        nq = 0
        Q = []
        # Точки очередного ребра отсекателя
        clip_fir = cutter[i]
        clip_sec = cutter[(i + 1) % len(cutter)]
        # Внутренняя нормаль к очередной границе отсекателя
        normal = inside_normal(cutter[i], cutter[(i + 1) % len(cutter)], cutter[(i + 2) % len(cutter)])
        # запоминаем первую вершину многоугольника
        F = obj[0]
        for j in range(len(obj)):
            if j > 0:
                # Если нашли пересечение ребра и границы отсекателя, нужно занести пересечение
                if check_intersection(S, obj[j], clip_fir, clip_sec, normal):
                    intersection = get_intersection(S, obj[j], clip_fir, clip_sec)
                    Q.append(intersection)
                    nq += 1
            # Назначаем новую конечную точку
            S = obj[j]
            # Проверяем ее видимость
            if check_visible(S, normal, clip_fir, clip_sec):
                Q.append(S)
                nq += 1
        if len(Q) == 0:
            return None
        if check_intersection(S, F, clip_fir, clip_sec, normal):
            intersection = get_intersection(S, F, clip_fir, clip_sec)
            Q.append(intersection)
            nq += 1
        obj = Q
    return obj
