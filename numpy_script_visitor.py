import re
import ast, _ast, astunparse


class NumpyScriptVisitor(ast.NodeTransformer):
    
    def __init__(self):
        super(NumpyScriptVisitor, self).__init__()
        self.replPair = {}
        self.semanticPatterns = {
            "'#1'.reshape('#2','#3')": "tf.reshape('#1',['#2','#3'])"
        }        
        
    def print_node(self, node):
        print(astunparse.unparse(node).strip())
        
    def func_substitution(self, node):
        """substitute function with corresponding new function name"""
        funcSubDict = {"arange": "range"}
        if type(node) == ast.Call:
            for funcName in funcSubDict.keys():
                if (node.func.attr == funcName):
                    node.func.attr = funcSubDict[funcName]

                
    def modify_import(self, node):
        if type(node) == ast.alias and node.name=="numpy":
            if not node.asname is None:
                node.asname = "tf"
                node.name = "tensorflow"
    
    def modify_numpy_asnames(self, node):
        if type(node) == ast.Name:
            if node.id == "np" and type(node.ctx) == ast.Load:
                node.id = "tf"
    
    def obj_type(self, node):
        if isinstance(node, ast.AST):
            result = str(node)
            result = result[6:result.find(" ")].strip()
            return result
        return None

    def seek_param(self, node, paramName):
        result = []
        self._seek_param(node, paramName, "", result)
        if (len(result)>0):
            return result[0]
        else:
            return None

    def _seek_param(self, node, paramName, path, result):
        #print(path)
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                id = 0
                for item in value:
                    if isinstance(item, ast.AST):
                        self._seek_param(item, paramName, (path+"."+str(field)+"["+str(id)+"]"), result)
                    else:
                        if (type(item) == paramName):
                            result.append(path+"."+field+"["+str(id)+"]")
                    id += 1
            elif isinstance(value, ast.AST):
                self._seek_param(value, paramName, path+"."+field, result)
            else:
                if (value == paramName):
                    result.append(path)
    
    
    def func_find_reconstruction_fields(self, scriptSlice):
        result = re.findall( r"'#[0-9]+'", scriptSlice)
        result = list(set(result))
        result = [item.replace("'","") for item in result]
        return result
        
    def func_reconstruction(self, node):
        if type(node) == ast.Call:
            for key in self.semanticPatterns.keys():
                fromPattern = key
                toPattern = self.semanticPatterns[key]
                
                funcName = re.findall( r"[.][^(]*", fromPattern)[0][1:]
    
                fromAst = ast.parse(fromPattern)
                toAst = ast.parse(toPattern)
                
                
                if (node.func.attr == funcName):
                    params = self.func_find_reconstruction_fields(fromPattern)
                    
                    for param in params:
                        fromPath = "node" +self.seek_param(fromAst, param)[14:]
                        toPath = "toAst"+self.seek_param(toAst, param)                    
                        exec("%s=%s" % (toPath, fromPath))
                    
                    
                    
                    asIs = astunparse.unparse(node).strip()
                    # self.print_node(node)
                    node = toAst.body[0].value
                    toBe = astunparse.unparse(node).strip()
                    # self.print_node(node)
                    
                    # store these pairs for future replacement
                    self.replPair[asIs] = toBe
            
                
    
    def generic_visit(self, node):
        self.modify_import(node)
        self.modify_numpy_asnames(node)
        self.func_substitution(node)
        self.func_reconstruction(node)
        
        # print(node)
            
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)

if __name__ == "__main__":
    import re
    a = "'#1'.reshape('#2','#3')"
    m = re.findall( r"[.][^(]*", a)
    print(m)



