from z3 import *
import re

class Z3_Worker():

    def info_on_expression(self, expression):
        regex = r'\b[^\d\W]+\b'
        varibles = re.findall(regex, expression)

        varibles = set(varibles)

        return varibles
    
    def simplify_tool(self, expression):
        expression_list = []
        modifier = self.char_in_str(expression, ['>', '<', '='])
        final_modifier = ''
        if modifier != False:
            if modifier in ['>', '<', '=']:
                if self.char_in_str(expression, ['=']):
                    final_modifier = modifier + '='
                    expression_list = expression.split(modifier+'=')
                else:
                    final_modifier = modifier
                    expression_list = expression.split(modifier)
            # hold simplified expression
            simplified_expressions = []
            # keep track of declared varibles to not dupe
            declared_vars = []
            # declare new varibles and add statements to solver
            # simplify each side and add it to a list
            for index, expression in enumerate(expression_list):
                varibles = self.info_on_expression(expression)

                for var in [x for x in varibles if x not in declared_vars]:
                    declared_vars.append(var)
                    exec(var + " = Real('"+var+"')")

                f = eval(expression)
                if type(f) == z3.z3.ArithRef:
                    simplified = simplify(f)
                else:
                    simplified = f
                
                if type(simplified) == z3.z3.BoolRef:
                    if simplified or not simplified:
                        simplified_expressions.append(expression_list[index])
                else:
                    simplified_expressions.append(simplified)
            # simplify the combined statements
            combined_expression = eval(final_modifier.join([str(elem) for elem in simplified_expressions]))
            if combined_expression == True:
                return final_modifier.join([str(elem) for elem in simplified_expressions])
            final_expression = simplify(combined_expression)
            if str(final_expression) == 'True' or str(final_expression) == 'False':
                if final_expression or not final_expression:
                    return str(combined_expression)
            else:
                return final_expression
        else:
            # keep track of declared varibles to not dupe
            declared_vars = []
            varibles = self.info_on_expression(expression)
            for var in [x for x in varibles if x not in declared_vars]:
                    exec(var + " = Real('"+var+"')")

            return simplify(eval(expression))
    def convert_or_to_z3_or(self, expression):
            if 'or' in expression.lower():
                expression = expression.lower().replace(' or ', ',')
                expression = "["+ expression+"]"
                status = True
            else:
                status = False
            
            return (status, expression)
    #returns sat if property is true for all values within the bounds
    #calls get_counterexample, if counter exists, for all is unsat; return unsat and counter
    #if counter exists, return sat
    def for_all(self):
        pass

    #takes statements and negates them
    #returns counterexample if it exists, otherwise sat
    def get_counterexample(self, expressions, bounds=[]):
        vars = set()
        for expression in expressions:
            for var in self.info_on_expression(expression):
                vars.add(var)

        for bound in bounds:
            for var in self.info_on_expression(bound):
                vars.add(var)
        
        s = Solver()

        for var in vars:
            executable = var + "=Real('" + var + "')"
            exec(executable)
        
        exprInput = "Not("
        for expression in expressions:
            exprInput += expression + ','
        
        exprInput = exprInput[0:len(exprInput) - 1] + ')'

        s.add(eval(exprInput))

        for bound in bounds:
            s.add(eval(bound))
        
        res = s.check()
        model = None
        if res == sat:
            model = s.model()
        
        return {"status":res, "counter":model}

if __name__ == '__main__':
    test = Z3_Worker()
    print(test.get_counterexample(["x+y>0"]))
