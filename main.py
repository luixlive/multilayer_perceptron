import sys
sys.path.append('libraries')

from itertools import product
from json import loads
from shutil import copyfile
from multilayer_perceptron import multilayerPerceptron

# Capture dynamic parameters
def getDynamicParameters(parameters):
  parametersDict = dict()
  for k, v in [p.split('=') if '=' in p else [p, True] for p in parameters]:
    if k[0] == '-':
      parametersDict[k[1:]] = v
    else:
      print 'ERROR: Wrong param ' + k
  return parametersDict

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
  if len(argv) == 0:
    argv.append('--help')

  command = argv[0]
  parameters = dict()
  if len(argv) > 1:
    parameters = getDynamicParameters(argv[1:])

  if command == '--help':
    commands_file = open('.json/commands.json', 'r')
    commands = loads(commands_file.read())
    commands_file.close()

    showHelp(commands)
  elif command == '--input':
    if 'f' in parameters:
      generateInputFile(parameters['f'])
    else:
      print '--input needs parameter -f for the generated input file\'s name'
  elif command == '--run':
    if 'i' not in parameters:
      print '--run needs parameter -i for the input file\'s name'
    else:
      constants_file = open('.json/constants.json', 'r')
      constants = loads(constants_file.read())
      constants_file.close()

      (x, d, x2) = readInputFile(parameters['i'])

      alpha = constants['alpha']
      maxError = constants['maxError']
      if 'a' in parameters:
        alpha = float(parameters['a'])
      if 'm' in parameters:
        maxError = float(parameters['m'])
      print
      print '\n'.join(multilayerPerceptron(x, d, x2, alpha, maxError, True))
      print


if __name__ == "__main__":
   main(sys.argv[1:])
