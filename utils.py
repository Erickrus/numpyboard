import ast


#using function signature can better differentiate two functions
def getFunctionSignature(funcNode):
    if type(funcNode)!=ast.Call:
        raise RuntimeError()
    funcSignature=""
    if hasattr(funcNode.func.value,'s'):
        funcSignature+=funcNode.func.value.s
    if hasattr(funcNode.func.value,'id'):
        funcSignature+=funcNode.func.value.id
    
    return funcSignature+funcNode.func.attr+str(len(funcNode.args))+str(len(funcNode.keywords))

