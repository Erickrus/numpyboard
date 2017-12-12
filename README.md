This is the very first version of numpyboard, which is inspired by tensorboard and is trying to reuse tensorboard to visualize the numpy calculation in a graph mode.
The idea is simply convert a numpy calculation to a tensorflow calculation, in the meanwhile, the script is automatically converted to the computational graph and get displayed.
Some issues, there're some calculation that doesnt work well in terms of the definition of 2 libraries. Two tricky way is applied to translate the code.
1. simply replace the function name to equivalent functions
2. using some wrap library to handle this.
