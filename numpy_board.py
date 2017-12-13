import os
import ast
import astunparse
from numpy_script_visitor import NumpyScriptVisitor

class NumpyBoard:
    
    def __init__(self, logDir, varName):
        self.logDir = logDir
        self.varName = varName
        try:
            os.system("rm %s/*tfevent*" % self.logDir)
            os.mkdir(self.logDir)
        except:
            pass
    
    def translate(self, numpyScript):
        numpyAst = ast.parse(numpyScript)
        nsv = NumpyScriptVisitor()
        nsv.visit(numpyAst)
        result = astunparse.unparse(numpyAst)
        
        for replFrom in nsv.replPair:
            replTo = nsv.replPair[replFrom]
            result = result.replace(replFrom, replTo)
        
        sessScript = "\n".join(
            ["",
            """logDir = "%s" """ % self.logDir,
            """sess = tf.Session()""",
            """sess.run(tf.global_variables_initializer())""",
            """sess.run(%s)""" % self.varName,
            """writer = tf.summary.FileWriter(logDir, sess.graph)""",
            """sess.close()"""])
        return result + sessScript
    
    def launch_numpyboard(self):
        os.system("cd %s && tensorboard --logdir ." % self.logDir)
        

if __name__ == "__main__":
    expr =  "\n".join([ 
        """import numpy as np""",
        "",
        """a = np.arange(6)""",
        """b = a.reshape(2,3*25)""",
        """a = (a + 100) * a"""
    ])

    nb = NumpyBoard("/home/eric/test", "a")
    
    print(expr)
    print("------------")
    res = nb.translate(expr)
    print(res)
    #exec(res)
    #nb.launch_numpyboard()
    
