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