import math


# based off of Graphics Gems Roots3And4.c
# https://github.com/erich666/GraphicsGems/blob/master/gems/Roots3And4.c

def cube_root(x):
    if x >= 0:
        return(x ** (1/3))
    else:
        return(-((-x) ** (1/3)))

def quadratic_solver(a, b, c):
    p = b / (2 * a)
    q = c / a
    D = (p * p) - q
    if math.isclose(D, 0, rel_tol=1e-09, abs_tol=1e-09):
        return [-p]
    elif D < 0:
        return []
    else:
        sqrt_D = math.sqrt(D)
        return [-sqrt_D - p, sqrt_D - p]


def cubic_solver(a, b, c, d):
    # reduce to normal form: y = x^3 + Ax^2 + Bx + C = 0
    A = b / a
    B = c / a
    C = d / a

    # substitute x = y - A/3 to eliminate quadric term:
    #   x^3 + px + q = 0

    sq_A = A * A
    p = (1/3) * (((-1/3) * sq_A) + B)
    q = (1/2) * (((2/27) * A * sq_A) - ((1/3) * A * B) + C)

    # use Cardano's formula - e.g. https://www.mathemania.com/lesson/cardanos-formula-solving-cubic-equations/
    # note that the 1/3 and 1/2 are added to p and q respectively because the
    # discriminant is (q/2) ^ 2 + (p/3) ^ 3 in the original formula and adding the 1/3
    # and 1/2 above is fewer multiplications
    cube_p = p * p * p
    D = q * q + cube_p

    if math.isclose(D, 0, rel_tol=1e-09, abs_tol=1e-09):
        if math.isclose(q, 0, rel_tol=1e-09, abs_tol=1e-09):
            # one triple solution
            res = [0]
        else:
            # one single and one double solution
            u = cube_root(-q)
            res = [2 * u, -u]
    elif D < 0:
        # three real solutions
        phi = (1/3) * math.acos(-q / math.sqrt(-cube_p))
        t = 2 * math.sqrt(-p)
        res = [t * math.cos(phi), -t * math.cos(phi + (math.pi/3)), -t * math.cos(phi - (math.pi/3))]
    else:
        # one real solution
        sqrt_D = math.sqrt(D)
        u = cube_root(sqrt_D - q)
        v = -cube_root(sqrt_D + q)
        res = [u + v]

    # resubstitute
    sub = (1/3) * A
    return [i - sub for i in res]


def quartic_solver(a, b, c, d, e):
    # reduce to normal form: x^4 + Ax^3 + Bx^2 + Cx + D = 0
    A = b / a
    B = c / a
    C = d / a
    D = e / a

    # substitute x = y - A/4 to eliminate the cubic term:
    # x^4 + px^2 + qx + r = 0

    sq_A = A * A
    p = (-3/8) * sq_A + B
    q = ((1/8) * (sq_A * A)) - ((1/2) * A * B) + C
    r = ((-3/256) * (sq_A * sq_A)) + ((1/16) * sq_A * B) - ((1/4) * A * C) + D

    if math.isclose(r, 0, rel_tol=1e-09, abs_tol=1e-09):
        # no absolute term: y(y^3 + py + q) = 0
        res = cubic_solver(1, 0, p, q)
        if not math.isclose(res[0], 0, rel_tol=1e-09, abs_tol=1e-09):
            res.append(0)
    else:
        # solve the resolvent cubic ...
        cub = cubic_solver(1, (-1/2) * p, -r, ((1/2) * r * p) - ((1/8) * q * q))
        # ... and take the one real solution ...
        z = cub[0]
        # ... to build two quadric equations
        u = (z * z) - r
        v = (2 * z) - p

        if math.isclose(u, 0, rel_tol=1e-09, abs_tol=1e-09):
            u = 0
        elif u > 0:
            u = math.sqrt(u)
        else:
            return []

        if math.isclose(v, 0, rel_tol=1e-09, abs_tol=1e-09):
            v = 0
        elif v > 0:
            v = math.sqrt(v)
        else:
            return []

        firstquadric = quadratic_solver(1, -v if q < 0 else v, z - u)
        secondquadric = quadratic_solver(1, v if q < 0 else -v, z + u)
        res = firstquadric + secondquadric

    # resubstitute
    sub = (1/4) * A
    return [i - sub for i in res]
