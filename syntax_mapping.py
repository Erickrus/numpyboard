####################################################################
# Script    : SyntaxMapping
# PURPOSE   : Syntax definition for translation
#
# CREATED:    2017-12-12    Eric Hu (hyinghao@hotmail.com)
#
#
# MODIFIED 
# DATE        AUTHOR            DESCRIPTION
# -------------------------------------------------------------------
# 
#####################################################################

import ast

import utils
class SyntaxMapping:
    def __init__(self):
        self.reconstructSyntax = {
            "'#1'.reshape('#2','#3')":
            "tf.reshape('#1',['#2','#3'])"
        }
        self.funcSubstituteDict = {
            "arange": "range"
        }
        self.reconstructFieldPattern = r"'#[0-9]+'"
        self.reconstructFuncPattern = r"[.][^(]*"
        #cache the sourcePattern appeared in self.reconstructSyntax, which is convenient to use
        self.reconstructFuncSignature=[]
        for sourcePattern in self.reconstructSyntax.keys():
            sourceFunc=ast.parse(sourcePattern).body[0].value
            funcSignature=utils.getFunctionSignature(sourceFunc)
            self.reconstructFuncSignature.append(funcSignature)

if __name__=='__main__':
    sm=SyntaxMapping()
    print sm.reconstructFuncSignature
