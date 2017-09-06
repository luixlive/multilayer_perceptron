import sys
sys.path.append('libraries')

from itertools import product
from json import loads
from shutil import copyfile
from multilayer_perceptron import multilayerPerceptron

# Print all commands in output
def showHelp(commands):
  print
  for command in commands:
    print '--' + command
    print '\t' + commands[command]['definition']
    print '\t' + 'Params: ' + ', '.join(commands[command]['params'])
    print '\t' + 'Optional params: ' + \
      ', '.join(commands[command]['optionalParams'])
  print

# Copy the input template file to the path given
def generateInputFile(name):
  copyfile('.input_file_template/input_file_template.txt', name)

# Transform the input file table format into matrixes 'x', 'd' and 'x2'
def extractXDX2(tableLines):
  x = list()
  d = list()
  rowCount = 0
  for row in [l.strip().split(' ') for l in tableLines]:
    xTemp = list()
    dTemp = list()
    inputs = True
    for value in row:
      if value == '|':
        inputs = False
      elif inputs:
        xTemp.append(bool(int(value)))
      else:
        dTemp.append(float(value))
    x.append(tuple(xTemp))
    d.append(tuple(dTemp))

    rowCount += 1

  truthTable = list(product([False, True], repeat=len(x[0])))
  x2 = [l for l in truthTable if l not in x]

  return (x, d, x2)

# Read an input file and extract the table into matrixes 'x', 'd' and 'x2'
def readInputFile(inputFilePath):
  inputFile = open(inputFilePath, 'r')
  input = inputFile.read().splitlines()
  inputFile.close()

  return extractXDX2([l for l in input if len(l.strip()) > 0 and l[0] != '#'])

# Main function, receives the input arguments and determines the code to run
def main(argv):
  if len(argv) == 0 or argv[0] == '--help':
    commands_file = open('.json/commands.json', 'r')
    commands = loads(commands_file.read())
    commands_file.close()

    showHelp(commands)
  elif argv[0] == '--input':
    if len(argv) >= 2:
      generateInputFile(argv[1])
    else:
      print '--input needs 1 parameter for the generated input file\'s name'
  elif argv[0] == '--run':
    if len(argv) < 2:
      print '--run needs 1 parameter for the input file\'s name'
    else:
      constants_file = open('.json/constants.json', 'r')
      constants = loads(constants_file.read())
      constants_file.close()

      (x, d, x2) = readInputFile(argv[1])

      alpha = constants['alpha']
      maxError = constants['maxError']
      if len(argv) > 2:
        alpha = float(argv[2])
      if len(argv) > 3:
        maxError = float(argv[3])
      print
      print '\n'.join(multilayerPerceptron(x, d, x2, alpha, maxError, True))
      print


if __name__ == "__main__":
   main(sys.argv[1:])
