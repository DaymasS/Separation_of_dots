def count_delta_vect(crds_list, i1, i2):
    upper = 0
    lower = 0
    x1 = crds_list[i2][0] - crds_list[i1][0]
    y1 = crds_list[i2][1] - crds_list[i1][1]
    for i in range(len(crds_list)):
        if (i != i1 and i != i2):
            x2 = crds_list[i][0] - crds_list[i1][0]
            y2 = crds_list[i][1] - crds_list[i1][1]
            vect_sign = x1 * y2 - x2 * y1
            if (vect_sign > 0):
                upper += 1
            elif (vect_sign < 0):
                lower += 1
    return abs(upper - lower)

def calc_coef(x1, y1, x2, y2):
    if (x1 == x2):
        k = None
        b = x1
    else:
        k = (y1 - y2) / (x1 - x2)
        b = y1 - k * x1
    return k, b


def search_line(crds_list):
    length = len(crds_list)
    min_delta = length
    if (length <= 1):
        return 1, 0, 0
    for i in range(length):
        for j in range(i + 1, length):
            cur_delta = count_delta_vect(crds_list, i, j)
            if (cur_delta < min_delta):
                min_delta = cur_delta
                i1 = i
                i2 = j
    k, b = calc_coef(crds_list[i1][0], crds_list[i1][1], crds_list[i2][0], crds_list[i2][1])
    return 0, k, b