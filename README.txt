Multilayer Perceptron
Luis Alfonso Chávez Abbadie
Sep 03, 2017

This project runs in Python 2.

Help:
  - Open project in terminal
  - Run 'python main.py --help' to get the list of commands

Example of usage:
  - Open project in terminal
  - Create an input file:
    'python main.py --input file_name.txt’
  - Open and follow the instructions in file_name to set your input table.
    Example:
      0 0 | 0
      0 1 | 1
      1 1 | 1
  - Run the multilayer perceptron running one of these commands:
    'python main.py --run file_name.txt'
    'python main.py --run file_name.txt alpha' (alpha is a number)
    'python main.py --run file_name.txt alpha maxError' (maxError is a number)
  - Check the results in the output

Multilayer Perceptron Algorithm:
  - Algorithm used in this project is mathematically explained in
    multilayer_perceptron_formulas.pdf
