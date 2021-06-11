from sympy import symbols, Eq, solve
import re


def info_on_expression(expression):
    regex = r'\b[^\d\W]+\b'
    varibles = re.findall(regex, expression)

    varibles = set(varibles)

    return varibles

def break_down_expression(expression):
    return (expression.split('=')[0].strip(),expression.split('=')[1].strip())

# input bound dict and expression dict
# bounds = {"y": 4, "y":16} # expression = {"y": "x ** 2"}
def find_bounds(bounds, expression):
    declared_vars = []
    solution_list = []

    # declare varibles
    varibles = info_on_expression(expression)
    
    for var in varibles:
        for var in [x for x in varibles if x not in declared_vars]:
            declared_vars.append(var)
            exec(var + " = symbols('"+var+"')")

    # expression
    broke_down = break_down_expression(expression)
    master_eq = Eq(eval(broke_down[1]), locals()[broke_down[0]])

    for bound in bounds:
        broke_down = break_down_expression(bound)
        bound_eq = Eq(eval(broke_down[1]), locals()[broke_down[0]])
        solution = solve((master_eq, bound_eq), [locals()["x"] for x in declared_vars])
        solution_list.append(solution)

    print(solution_list)

if __name__ == '__main__':
    find_bounds(['y=4','y=16'], 'y=x**2')