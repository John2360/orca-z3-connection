from sympy import symbols, Eq, solve
import re

def info_on_expression(expression):
    regex = r'\b[^\d\W]+\b'
    varibles = re.findall(regex, expression)

    varibles = set(varibles)

    return varibles

# split code line by line
def code_to_list(code):
    return code.split(',')

def break_down_expression(expression):
    return (expression.split('=')[0].strip(),expression.split('=')[1].strip())

def find_bounds_input(expression):
    code_lines = code_to_list(expression)

    expression_list = []
    bounds_list = []
    
    for index, expression in enumerate(code_lines):
        char = char_in_str(expression, ['>', '<', '='])
        if char == '>' or char == '<' or char == '=':
            code_lines[index] = expression.split(char)
            
            for code in code_lines[index]:
                varibles = info_on_expression(code)

                if(len(varibles) > 0):
                    expression_list.append("y="+code)
                else:
                    bounds_list.append("y="+code)

    return (bounds_list, expression_list[0])

def char_in_str(input, list):
    for char in list:
        if char in input:
            return char
    return False

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

    return solution_list

if __name__ == '__main__':
    print(find_bounds_input('x**2>4,x**2<16'))
    bounds, expression = find_bounds_input('x**2>4,x**2<16')
    print(find_bounds(bounds, expression))