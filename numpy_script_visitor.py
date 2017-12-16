####################################################################
# Script    : NumpyScriptVisitor
# PURPOSE   : Numpy script translator
#             Somehow could be used as generic syntax replacement tool
#
# CREATED:    2017-12-12    Eric Hu (hyinghao@hotmail.com)
#
#
# MODIFIED 
# DATE        AUTHOR            DESCRIPTION
# -------------------------------------------------------------------
# 
#####################################################################
import re
import ast, _ast, astunparse

from syntax_mapping import SyntaxMapping
import utils

class NumpyScriptVisitor(ast.NodeTransformer):
    
    def __init__(self):
        # override NodeTransformer's original init function
        super(NumpyScriptVisitor, self).__init__()
        self.replaceSnippet = {}
        self.syntaxMapping = SyntaxMapping()

        
    def print_node(self, node):
        # print the node
        print(astunparse.unparse(node).strip())
        
    def func_substitute(self, node):
        # substitute function with corresponding new function name
        if type(node) == ast.Call:
            for funcName in self.syntaxMapping.funcSubstituteDict.keys():
                if (node.func.attr == funcName):
                    node.func.attr = self.syntaxMapping.funcSubstituteDict[funcName]

    def modify_import(self, node):
        # modify the imports by replacing the import statement
        if type(node) == ast.alias and node.name=="numpy":
            if not node.asname is None:
                node.asname = "tf"
                node.name = "tensorflow"
    
    def modify_asnames(self, node):
        # modify prefix of np
        if type(node) == ast.Name:
            if node.id == "np" and type(node.ctx) == ast.Load:
                node.id = "tf"

    def seek_param(self, node, paramName):
        # seek for given param by traversing the node tree
        result = []
        # initially, just pass empty path and empty result
        # result will be changed during the process, if any param is found
        self._seek_param(node, paramName, "", result)
        if (len(result)>0):
            return result[0]
        else:
            return None

    def _seek_param(self, node, paramName, path, result):
        # Recursive function defined to seek param
        # This function is defined based on generic_visit()
        # Basically, the idea is inspired by xpath
        # Path is designed to refer to the relative position in the tree
        for field, value in ast.iter_fields(node):
            # for list items
            if isinstance(value, list):
                idx = 0
                for item in value:
                    if isinstance(item, ast.AST):
                        self._seek_param(item, paramName, (path+"."+str(field)+"["+str(idx)+"]"), result)
                    else:
                        if (item == paramName):
                            # usually this will not be accessed
                            result.append(path+"."+field+"["+str(idx)+"]")
                    idx += 1
            # for normal items
            elif isinstance(value, ast.AST):
                self._seek_param(value, paramName, path+"."+field, result)
            # for the leaf nodes
            else:
                if (value == paramName):
                    result.append(path)
    
    
    def _find_reconstruct_fields(self, node):
        # find all patterns for reconstruct fields, and replace additional quotes
        result=[]
        for i in ast.walk(node):
            if hasattr(i,'id'):
                result.append(i.id)
        return result
        
    def func_reconstruct(self, node):
        
        # reconstruct node structure based on the given reconstruct syntax
        if type(node) == ast.Call:
            #get the signature of this function node
            nodeFuncSignature=utils.getFunctionSignature(node)
            for keyIndex,key in enumerate(self.syntaxMapping.reconstructSyntax.keys()):
                sourcePattern = key
                targetPattern = self.syntaxMapping.reconstructSyntax[key]
                # scanning for the function name in the pattern
                
                sourceAst = ast.parse(sourcePattern)
                targetAst = ast.parse(targetPattern)
                
                if (nodeFuncSignature == self.syntaxMapping.reconstructFuncSignature[keyIndex]):
                    params = self._find_reconstruct_fields(sourceAst)
                    
                    for para_index,param in enumerate(params):
                        sourcePath = "node" +self.seek_param(sourceAst, param)[14:]
                        targetPath = "targetAst"+self.seek_param(targetAst, param)
                        # assign the node's corresponding sub-node to the target node
                        # and this will generate a template for later replacement
                        exec("%s=%s" % (targetPath, sourcePath))
                    
                    
                    
                    oldSnippet = astunparse.unparse(node).strip()
                    # make sure the function part of the target is on it's body[0]
                    # this is somehow hard-coded
                    node = targetAst.body[0].value
                    newSnippet = astunparse.unparse(node).strip()

                    #print ('#'*10)
                    #print (oldSnippet)
                    #print (newSnippet)
                    #print ('#'*10)
                    
                    # store these pairs for future replacement
                    self.replaceSnippet[oldSnippet] = newSnippet
            
    def generic_visit(self, node):
        # override the original generic_visit function
        self.modify_import(node)
        self.modify_asnames(node)
        self.func_substitute(node)
        self.func_reconstruct(node)
            
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)



