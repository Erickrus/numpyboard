
from numpy_board import NumpyBoard

if __name__ == "__main__":
    npSnippet =  "\n".join([ 
        """import numpy as np""",
        "",
        """a = np.arange(6)""",
        """a = a.reshape(2,3*1)""",
        """a = (a + 100) * a"""
    ])

    nb = NumpyBoard("/home/haijun/tmp/tmp/log", "a")
    
    print(npSnippet)
    print("------------")
    res = nb.run_tfgraph(npSnippet)
    nb.launch_numpyboard()
