def supercover_line(p0, p1):
    dx = p1[0]-p0[0]
    dy = p1[1]-p0[1]
    nx = abs(dx)
    ny = abs(dy)
    sign_x = 1 if dx > 0 else -1
    sign_y = 1 if dy > 0 else -1

    p = [p0[0], p0[1]]
    points = []
    ix = 0
    iy = 0

    while (ix < nx or iy < ny):

        decision = (1 + 2*ix) * ny - (1 + 2*iy) * nx
        if (decision == 0):
            # next step is diagonal
            p[0] += sign_x
            p[1] += sign_y
            ix += 1
            iy += 1
        elif (decision < 0):
            # next step is horizontal
            p[0] += sign_x
            ix += 1
        else:
            # next step is vertical
            p[1] += sign_y
            iy += 1

        points.append((p[0],p[1]))
    return points