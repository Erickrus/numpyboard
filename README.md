This is the very first version of numpyboard, which is inspired by tensorboard and is trying to reuse tensorboard to visualize the numpy calculation in a graph mode.
The idea is simply convert a numpy calculation to a tensorflow calculation, in the meanwhile, the script is automatically converted to the computational graph and get displayed.
Some issues, there're some calculation that doesnt work well in terms of the definition of 2 libraries. Two tricky way is applied to translate the code.
1. simply replace the function name to equivalent functions
2. using some wrap library to handle this.

e.g.
```python
import numpy as np

a = np.arange(6)
a = (a + 100) * a
```

will be translated into
```python
import tensorflow as tf
a = tf.range(6)
a = ((a + 100) * a)

logDir = "/home/eric/test"
sess = tf.Session()
sess.run(tf.global_variables_initializer())
sess.run(a)
writer = tf.summary.FileWriter(logDir, sess.graph)
sess.close()
```

![tf-result](img/tf-result.png?raw=true)