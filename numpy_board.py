####################################################################
# Script    : NumpyBoard
# PURPOSE   : Leverage tensorboard to display the numpy computational graph
#
# CREATED:    2017-12-12    Eric Hu (hyinghao@hotmail.com)
#
#
# MODIFIED 
# DATE        AUTHOR            DESCRIPTION
# -------------------------------------------------------------------
# 
#####################################################################
import os
import ast
import datetime
import astunparse


from numpy_script_visitor import NumpyScriptVisitor

class NumpyBoard:
    
    def __init__(self, logDir, varName):
        self.logDir = logDir
        self.varName = varName
        try:
            # try to remove the corresponding tfevent
            os.system("rm %s/*tfevent*" % self.logDir)
            os.mkdir(self.logDir)
        except:
            pass
    
    def _translate(self, numpyScript):
        # translate numpy script to tensorflow script
        numpyAst = ast.parse(numpyScript)
        nsv = NumpyScriptVisitor()
        nsv.visit(numpyAst)
        result = astunparse.unparse(numpyAst)
        
        for oldSnippet in nsv.replaceSnippet:
            newSnippet = nsv.replaceSnippet[oldSnippet]
            result = result.replace(oldSnippet, newSnippet)
        
        sessScript = "\n".join(
            ["",
            """logDir = "%s" """ % self.logDir,
            """sess = tf.Session()""",
            """sess.run(tf.global_variables_initializer())""",
            """sess.run(%s)""" % self.varName,
            """writer = tf.summary.FileWriter(logDir, sess.graph)""",
            """sess.close()"""])
        return result + sessScript
    
    def run_tfgraph(self, numpyScript):
        tfScript = self._translate(numpyScript)
        print(tfScript)
        filename = "/tmp/%s.py" % str(self._get_js_timestamp())
        self._save_file(filename, tfScript)
        os.system("cd /tmp && python3 %s" % filename)


    def _save_file(self, filename, content):
        f = open(filename,'wb')
        f.write(bytes(content, 'utf-8'))
        f.close()
        
    def _get_js_timestamp(self):
        # maybe you should change it correspondingly
        timezone_diff = 3600*8
        curr_datetime = datetime.datetime.now()
        epoch_datetime = datetime.datetime(1970,1,1)
        return int(((curr_datetime - epoch_datetime).total_seconds() - timezone_diff)*1000)

    
    def launch_numpyboard(self):
        print("cd %s && tensorboard --logdir ." % self.logDir)
        print("Starting TensorBoard and you can navigate to http://localhost:6006)")
        

    
