import ast

class NumpyScriptVisitor(ast.NodeTransformer):
    
    def modify_import(self, node):
        if type(node) == ast.alias and node.name=="numpy":
            if not node.asname is None:
                node.asname = "tf"
                node.name = "tensorflow"
    
    def modify_numpy_asnames(self, node):
        if type(node) == ast.Name:
            if node.id == "np" and type(node.ctx) == ast.Load:
                node.id = "tf"
    
    def modify_numpy_functions(self, node):
        if type(node) == ast.Call:
            if (node.func.attr == "arange"):
                node.func.attr = "range"

            #print(node.func.attr)
    
    def generic_visit(self, node):
        self.modify_import(node)
        self.modify_numpy_asnames(node)
        self.modify_numpy_functions(node)
        
        # print(node)
            
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)
