from sympy import symbols, Eq, solve


def find_bounds(bounds, expressions):
    x,y = symbols('x y')
    eq1 = Eq(x ** 2 - y)
    eq2 = Eq(4 - y)
    eq3 = Eq(16 - y)
    sol1 = solve((eq1,eq2), (x,y))
    sol2 = solve((eq1,eq3), (x,y))
    print(sol1, sol2)