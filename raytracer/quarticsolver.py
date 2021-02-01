# forked from https://github.com/NKrvavica/fqs/blob/master/fqs.py
# see MIT License: https://github.com/NKrvavica/fqs/blob/master/LICENSE
# Code is Copyright (c) 2019 NKrvavica

"""
MIT License

Copyright (c) 2019 NKrvavica

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import cmath
import math


def single_quadratic(a0, b0, c0):
    """ Analytical solver for a single quadratic equation
    (2nd order polynomial).
    Parameters
    ----------
    a0, b0, c0: array_like
        Input data are coefficients of the Quadratic polynomial::
            a0*x^2 + b0*x + c0 = 0
    Returns
    -------
    r1, r2: tuple
        Output data is a tuple of two roots of a given polynomial.
    """
    ''' Reduce the quadratic equation to to form:
        x^2 + ax + b = 0'''
    a, b = b0 / a0, c0 / a0

    # Some repating variables
    a0 = -0.5*a
    delta = a0*a0 - b
    sqrt_delta = cmath.sqrt(delta)

    # Roots
    r1 = a0 - sqrt_delta
    r2 = a0 + sqrt_delta

    return r1, r2


def single_cubic(a0, b0, c0, d0):
    """ Analytical closed-form solver for a single cubic equation
    (3rd order polynomial), gives all three roots.
    Parameters
    ----------
    a0, b0, c0, d0: array_like
        Input data are coefficients of the Cubic polynomial::
            a0*x^3 + b0*x^2 + c0*x + d0 = 0
    Returns
    -------
    roots: tuple
        Output data is a tuple of three roots of a given polynomial.
    """

    ''' Reduce the cubic equation to to form:
        x^3 + a*x^2 + b*x + c = 0 '''
    a, b, c = b0 / a0, c0 / a0, d0 / a0

    # Some repeating constants and variables
    third = 1./3.
    a13 = a*third
    a2 = a13*a13
    sqr3 = math.sqrt(3)

    # Additional intermediate variables
    f = third*b - a2
    g = a13 * (2*a2 - b) + c
    h = 0.25*g*g + f*f*f

    def cubic_root(x):
        """ Compute cubic root of a number while maintaining its sign"""
        if x.real >= 0:
            return x**third
        else:
            return -(-x)**third

    if f == g == h == 0:
        r1 = -cubic_root(c)
        return r1, r1, r1

    elif h <= 0:
        j = math.sqrt(-f)
        k = math.acos(-0.5*g / (j*j*j))
        m = math.cos(third*k)
        n = sqr3 * math.sin(third*k)
        r1 = 2*j*m - a13
        r2 = -j * (m + n) - a13
        r3 = -j * (m - n) - a13
        return r1, r2, r3

    else:
        sqrt_h = cmath.sqrt(h)
        S = cubic_root(-0.5*g + sqrt_h)
        U = cubic_root(-0.5*g - sqrt_h)
        S_plus_U = S + U
        S_minus_U = S - U
        r1 = S_plus_U - a13
        r2 = -0.5*S_plus_U - a13 + S_minus_U*sqr3*0.5j
        r3 = -0.5*S_plus_U - a13 - S_minus_U*sqr3*0.5j
        return r1, r2, r3


def single_cubic_one(a0, b0, c0, d0):
    """ Analytical closed-form solver for a single cubic equation
    (3rd order polynomial), gives only one real root.
    Parameters
    ----------
    a0, b0, c0, d0: array_like
        Input data are coefficients of the Cubic polynomial::
            a0*x^3 + b0*x^2 + c0*x + d0 = 0
    Returns
    -------
    roots: float
        Output data is a real root of a given polynomial.
    """

    ''' Reduce the cubic equation to to form:
        x^3 + a*x^2 + bx + c = 0'''
    a, b, c = b0 / a0, c0 / a0, d0 / a0

    # Some repeating constants and variables
    third = 1./3.
    a13 = a*third
    a2 = a13*a13

    # Additional intermediate variables
    f = third*b - a2
    g = a13 * (2*a2 - b) + c
    h = 0.25*g*g + f*f*f

    def cubic_root(x):
        """ Compute cubic root of a number while maintaining its sign
        """
        if x.real >= 0:
            return x**third
        else:
            return -(-x)**third

    if f == g == h == 0:
        return -cubic_root(c)

    elif h <= 0:
        j = math.sqrt(-f)
        k = math.acos(-0.5*g / (j*j*j))
        m = math.cos(third*k)
        return 2*j*m - a13

    else:
        sqrt_h = cmath.sqrt(h)
        S = cubic_root(-0.5*g + sqrt_h)
        U = cubic_root(-0.5*g - sqrt_h)
        S_plus_U = S + U
        return S_plus_U - a13


def single_quartic(a0, b0, c0, d0, e0):
    """ Analytical closed-form solver for a single quartic equation
    (4th order polynomial). Calls `single_cubic_one` and
    `single quadratic`.
    Parameters
    ----------
    a0, b0, c0, d0, e0: array_like
        Input data are coefficients of the Quartic polynomial::
        a0*x^4 + b0*x^3 + c0*x^2 + d0*x + e0 = 0
    Returns
    -------
    r1, r2, r3, r4: tuple
        Output data is a tuple of four roots of given polynomial.
    """

    ''' Reduce the quartic equation to to form:
        x^4 + a*x^3 + b*x^2 + c*x + d = 0'''
    a, b, c, d = b0/a0, c0/a0, d0/a0, e0/a0

    # Some repeating variables
    a0 = 0.25*a
    a02 = a0*a0

    # Coefficients of subsidiary cubic euqtion
    p = 3*a02 - 0.5*b
    q = a*a02 - b*a0 + 0.5*c
    r = 3*a02*a02 - b*a02 + c*a0 - d

    # One root of the cubic equation
    z0 = single_cubic_one(1, p, r, p*r - 0.5*q*q)

    # Additional variables
    s = cmath.sqrt(2*p + 2*z0.real + 0j)
    if s == 0:
        t = z0*z0 + r
    else:
        t = -q / s

    # Compute roots by quadratic equations
    r0, r1 = single_quadratic(1, s, z0 + t)
    r2, r3 = single_quadratic(1, -s, z0 - t)

    return r0 - a0, r1 - a0, r2 - a0, r3 - a0


def quadratic_solver(a, b, c):
    roots = single_quadratic(a, b, c)
    res = []
    for root in roots:
        if math.isclose(root.imag, 0) and root.real not in res:
            # only care about the real roots
            res.append(root.real)
    return res


def cubic_solver(a, b, c, d):
    roots = single_cubic(a, b, c, d)
    res = []
    for root in roots:
        if math.isclose(root.imag, 0) and root.real not in res:
            # only care about the real roots
            res.append(root.real)
    return res


def quartic_solver(a, b, c, d, e):
    roots = single_quartic(a, b, c, d, e)
    res = []
    for root in roots:
        if math.isclose(root.imag, 0, abs_tol=1e-02) and root.real not in res:
            # only care about the real roots.  Due to floating point math, we assume anything with a complex
            # part with absolute value of 0.01 or less is really a real root.
            res.append(root.real)
    return res
