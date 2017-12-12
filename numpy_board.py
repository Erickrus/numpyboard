import os
import ast
import astunparse
from numpy_script_visitor import NumpyScriptVisitor

class NumpyBoard:
    
    def __init__(self, logDir):
        self.logDir = logDir
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
        sessScript = """
logDir = "%s"
sess = tf.Session()
sess.run(tf.global_variables_initializer())
sess.run(a)
writer = tf.summary.FileWriter(logDir, sess.graph)
sess.close()
""" % self.logDir
        return result + sessScript

if __name__ == "__main__":
    expr = """
import numpy as np

a = np.arange(6)
a = (a + 100) * a

    """


# tensorboard --logdir=.

    nb = NumpyBoard("/home/eric/test")
    res = nb.translate(expr)
    print(res)
