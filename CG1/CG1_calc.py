import math as m

def find_circles(fir_dots, sec_dots):
    # Массивы окружностей заданных тремя точками
    fir_circles = []
    sec_circles = []
    for fir_fir in range(0, len(fir_dots)):    # первая точка первой окружности
        for fir_sec in range(fir_fir + 1, len(fir_dots)):    # вторая точка первой окружности
            for fir_thi in range(fir_sec + 1, len(fir_dots)):    # третья точка первой окружности
                # проверка на то, выбраны три различные по координатам точки
                if check_equal(fir_dots[fir_fir][1], fir_dots[fir_sec][1], fir_dots[fir_thi][1]) == 0:
                    fir_circles.append([fir_dots[fir_fir], fir_dots[fir_sec], fir_dots[fir_thi]])

    for sec_fir in range(0, len(sec_dots)):  # первая точка второй окружности
        for sec_sec in range(sec_fir + 1, len(sec_dots)):  # вторая точка второй окружности
            for sec_thi in range(sec_sec + 1, len(sec_dots)):  # третья точка второй окружности
                # проверка на то, выбраны ли разные по координатам точки
                if check_equal(sec_dots[sec_fir][1], sec_dots[sec_sec][1], sec_dots[sec_thi][1]) == 0:
                    sec_circles.append([sec_dots[sec_fir], sec_dots[sec_sec], sec_dots[sec_thi]])

    '''Теперь для каждой пары окружностей найдем их центры, а после проверим их касательные на параллельность
    оси Ох, не забыв проверить что одна окружность не лежит внутри другой'''
    for i in range(0, len(fir_circles)):
        #print("i iter")
        fir_cnt_x, fir_cnt_y = find_center(fir_circles[i][0][1], fir_circles[i][1][1], fir_circles[i][2][1])
        if fir_cnt_x == None:
            continue
        for j in range(0, len(sec_circles)):
            sec_cnt_x, sec_cnt_y = find_center(sec_circles[j][0][1], sec_circles[j][1][1], sec_circles[j][2][1])
            if sec_cnt_x == None:
                continue

            x1 = fir_circles[i][0][1][0]    # координата по х одной из точек окружности
            y1 = fir_circles[i][0][1][1]    # координата по y одной из точек окружности
            r1 = ((x1 - fir_cnt_x)**2 + (y1 - fir_cnt_y)**2)**0.5    # вычисляем радиус первой окружности

            x2 = sec_circles[j][0][1][0]    # координата по х одной из точек окружности
            y2 = sec_circles[j][0][1][1]    # координата по y одной из точек окружности
            r2 = ((x2 - sec_cnt_x) ** 2 + (y2 - sec_cnt_y) ** 2) ** 0.5  # вычисляем радиус второй окружности

            dist = ((fir_cnt_x - sec_cnt_x) ** 2 + (fir_cnt_y - sec_cnt_y) ** 2) ** 0.5    # расстояние между центрами окружностей

            # проверка на то, что одна из окружностей лежит внутри другой (нельзя построить касательные)
            if r1 > r2 and (r2 + dist < r1):
                continue
            if r2 > r1 and (r1 + dist < r2):
                continue

            # получаем массив точек касания
            touch_points = find_touch_points([[fir_cnt_x, fir_cnt_y], r1], [[sec_cnt_x, sec_cnt_y], r2])

            # получаем массив с точками на окружностях
            points = [[], []]
            for elem in fir_circles[i]:
                points[0].append(elem)
            for elem in sec_circles[j]:
                points[1].append(elem)

            # получаем массив с описанием окружностей
            cir = [[fir_cnt_x, fir_cnt_y, r1], [sec_cnt_x, sec_cnt_y, r2]]

            # сами точки касания для последующей обработки
            T1 = touch_points[0][0]
            T2 = touch_points[0][1]
            T3 = touch_points[1][0]
            T4 = touch_points[1][1]

            if is_parallel(T1, T3) == 0 or is_parallel(T2, T4) == 0:
                # три массива с информацией о точках, с информацией о касательных, о окружностях
                # отправляем в ответ
                return points, touch_points, cir
    return None, None, None


# Функция проверяет, различные ли точки поданы на вход
def check_equal(dot1, dot2, dot3):
    if dot1 == dot2 or dot1 == dot3 or dot2 == dot3:
        return 1
    return 0


# Функция ищет координаты центра окружности по трем точкам этой окрудности
def find_center(dot1, dot2, dot3):
    #print(dot1, dot2, dot3)
    eps = 0.0001
    a = dot2[0] - dot1[0]    #x2 - x1
    b = dot2[1] - dot1[1]    #y2 - y1
    c = dot3[0] - dot1[0]    #x3 - x1
    d = dot3[1] - dot1[1]    #y3 - y1
    e = a * (dot1[0] + dot2[0]) + b * (dot1[1] + dot2[1])
    f = c * (dot1[0] + dot3[0]) + d * (dot1[1] + dot3[1])
    g = 2 * (a * (dot3[1] - dot2[1]) - b * (dot3[0] - dot2[0]))
    # если g в районе нуля, значит точки лежат на одной прямой и окружности не существует
    if abs(g) < eps:
        return (None, None)
    centerx = (d * e - b * f) / g
    centery = (a * f - c * e) / g
    return centerx, centery

# Функция находит четыре точки внешнего касания
# cir = [[centerx, centery], r]
def find_touch_points(cir1, cir2):
    x1 = cir1[0][0]
    y1 = cir1[0][1]
    r1 = cir1[1]

    x2 = cir2[0][0]
    y2 = cir2[0][1]
    r2 = cir2[1]

    # расстояние между окружностями
    dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    # углы смещения, по сути углы между Ох и направлениями на точки касания
    phi_plus = m.atan2(y2 - y1, x2 - x1) + m.acos((r1 - r2) / dist)
    phi_minus = m.atan2(y2 - y1, x2 - x1) - m.acos((r1 - r2) / dist)

    # рассчет координат точек касания для первой окружности
    T1x = x1 + r1 * m.cos(phi_plus)
    T1y = y1 + r1 * m.sin(phi_plus)
    T2x = x1 + r1 * m.cos(phi_minus)
    T2y = y1 + r1 * m.sin(phi_minus)

    # рассчет координат точек касания для второй окружности
    T3x = x2 + r2 * m.cos(phi_plus)
    T3y = y2 + r2 * m.sin(phi_plus)
    T4x = x2 + r2 * m.cos(phi_minus)
    T4y = y2 + r2 * m.sin(phi_minus)

    return [[[T1x, T1y], [T2x, T2y]], [[T3x, T3y], [T4x, T4y]]]


# функция проверяет прямую, заданную точками на параллельность Ох
def is_parallel(t1, t2):
    # считаем тангенс угла наклона прямой, берем сразу положительный
    eps = 0.0001
    # ДОБАВИТЬ ПРОВЕРКУ
    if abs(t1[0] - t2[0]) < eps:
        return 1
    tang = abs((t1[1] - t2[1]) / (t1[0] - t2[0]))
    # если тангенс близок к нулю, считаем что прямая параллельна
    if tang < eps:
        return 0
    return 1


# Функция ищет по двум введенным окружностям оптимальные интервалы
# по Х и У для отрисовки рисунка в центре квадратного холста
# pixmapx, pixmapy - количество пикселей, доступных по осям (натягиваем настоящие координаты на пиксельные)
def pixmap_params(fir_cir, sec_cir):
    fir_cnt_x = fir_cir[0]
    fir_cnt_y = fir_cir[1]
    r1 = fir_cir[2]

    sec_cnt_x = sec_cir[0]
    sec_cnt_y = sec_cir[1]
    r2 = sec_cir[2]

    # теперь найдем самую верхнюю, нижнюю, левую и правую координаты рисунка
    left = min(fir_cnt_x - r1, sec_cnt_x - r2)  # самая левая координата
    right = max(fir_cnt_x + r1, sec_cnt_x + r2)  # самая правая координата
    up = max(fir_cnt_y + r1, sec_cnt_y + r2)  # самая верхняя координата
    down = min(fir_cnt_y - r1, sec_cnt_y - r2)  # самая нижняя координата

    # так как вписывать будем в пиксельный квадратный холст, нужно чтобы координатный холст тоже был квадратныи
    # увеличиваем меньший промежуток до большего
    diff = abs((right - left) - (up - down))  # разница промежутков
    if right - left > up - down:
        up += diff / 2
        down -= diff / 2
    elif up - down > right - left:
        right += diff / 2
        left -= diff / 2
    width = right - left  # итоговая ширина и высота координатной сетки
    # также нужно включить в расчет небольшие зазоры, чтобы рисунок не пересекался с осями
    borders = width / 10

    up += borders
    down -= borders
    right += borders
    left -= borders

    return up, down, right, left
