from sympy import symbols, Eq, solve
import re
import string

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
    var_list = []
    possible_vars = list(string.ascii_lowercase)
    untaken_vars = [x for x in possible_vars if x not in var_list]
    
    for line in code_lines:
        varibles = info_on_expression(line)
        for var in varibles:
            var_list.append(var)

    for index, expression in enumerate(code_lines):
        char = char_in_str(expression, ['>', '<', '='])
        if char == '>' or char == '<' or char == '=':
            code_lines[index] = expression.split(char)
            
            for code in code_lines[index]:
                varibles = info_on_expression(code)
     
                if(len(varibles) > 0):
                    expression_list.append(code)
                else:
                    bounds_list.append(code)

    for expression in code_lines:
        if expression[0] == expression_list[0]:
            bounds_list.append(expression[1])
        elif expression[1] == expression_list[0]:
            bounds_list.append(expression[0])

    for index, item in enumerate(bounds_list):
        bounds_list[index] = untaken_vars[0] + "=" + item
    
    for index, item in enumerate(expression_list):
        expression_list[index] = untaken_vars[0] + "=" + item

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

def get_intervals(ineqs, intersections):
    points = []
    for list in intersections:
        for point in list:
            points.append(point)

    domainVals = [point[0] for point in points]
    domainVals.sort()
    domainVals.insert(0, domainVals[0] - 1)
    domainVals.append(domainVals[-1] + 1)

    intervals = []

    for i in range(0, len(domainVals) - 1):
        avg = (domainVals[i] + domainVals[i+1])/2
        isInterval = True
        for ineq in ineqs:
            if not plug_in(ineq, {"x":avg}):
                isInterval = False
                break
        
        if isInterval:
            start = domainVals[i]
            end = domainVals[i+1]
            igrouper = "["
            fgrouper = "]"
            if i + 1 == len(domainVals) - 1:
                end = "INF"
                fgrouper = ")"
            if i == 0:
                start = "-INF"
                igrouper = "("
            


            for ineq in ineqs:
                if not plug_in(ineq, {"x":domainVals[i]}):
                    igrouper = "("
                    break
            
            for ineq in ineqs:
                if not plug_in(ineq, {"x":domainVals[i+1]}):
                    fgrouper = ")"
                    break 


            intervals.append(igrouper+str(start) + ","+str(end)+fgrouper)

    return intervals
    
def plug_in(ineq, valDict):
    string = ineq
    for key in valDict:
        while key in string:
            string = string.replace(key, "("+str(valDict[key])+")")   

    answer = eval(string)
    return answer

def produce_counterexample(expressions):
    s = Solver()
        
    for expression in expressions:
        varibles = info_on_expression(expression)

        for var in varibles:
            exec(var + " = Real('"+var+"')")

        expression = expression.replace('=', '==')
        f = eval(expression)
        s.add(Not(f))
    
    s.check()
    return s.model()

        
    
    




if __name__ == '__main__':
    # print(find_bounds_input('x**2>4,x**2<16'))
    # bounds, expression = find_bounds_input('x**2>4,x**2<16')
    # print(find_bounds(bounds, expression))
    print("ints:",get_intervals(['x**2>4','x**2<16'], [[(-2, 4), (2, 4)], [(-4, 16), (4, 16)]]))

    # bounds, expression = find_bounds_input("-x**2 + 4 > x ** 2 - 4")
    # print(find_bounds(bounds, expression))