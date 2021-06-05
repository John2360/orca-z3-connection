import ast

class OperationsTree():
    def __init__(self, input):
        self.node = ast.parse(input) 

    def show_children(self, node, level=0):
        if isinstance(node, ast.Num):
            print(' ' * level + str(node.n))
        else:
            print(' ' * level + str(node))
        for child in ast.iter_child_nodes(node):
            self.show_children(child, level+1)