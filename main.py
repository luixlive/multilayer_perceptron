import sys
sys.path.append('libraries')

from itertools import product
from json import loads, dumps
from shutil import copyfile
from multilayer_perceptron import learningProcess, getY2

# Capture dynamic parameters
def getDynamicParameters(parameters):
  parametersDict = dict()
  for k, v in [p.split('=') if '=' in p else [p, True] for p in parameters]:
    assert k[0] == '-', 'ERROR: Wrong param ' + k
    parametersDict[k[1:]] = v
  return parametersDict

# Validate that user's input params have the required ones
def validateMandatoryParameters(mandatoryParams, inputParams, message):
  for param in mandatoryParams:
    assert param in inputParams, message

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
  copyfile('.templates/input_file_template.txt', name)

# Transform the input file table format into matrixes 'x' and 'd'
def extractXD(tableLines):
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

  return (x, d)

# Transform the output file table format into matrix 'x2'
def extractX2(tableLines):
  x2 = list()
  x2.append([l.strip().split(' ') for l in tableLines])
  return x2

# Read lines of a plain text file with # as comment lines, ignoring empty lines
def readTableFile(tableFilePath):
  tableFile = open(tableFilePath, 'r')
  table = tableFile.read().splitlines()
  tableFile.close()

  return [l for l in table if len(l.strip()) > 0 and l[0] != '#']

# Read an input file and extract the table into matrixes 'x', 'd' and 'x2'
def readInputFile(inputFilePath):
  return extractXD(readTableFile(inputFilePath))

# Read an output file and extract the table into matrix 'x2'
def readOutputFile(outputFilePath):
  return extractX2(readTableFile(outputFilePath))

# Main function, receives the input arguments and determines the code to run
def main(argv):
  if len(argv) == 0:
    argv.append('--help')

  command = argv[0]
  parameters = dict()
  if len(argv) > 1:
    parameters = getDynamicParameters(argv[1:])

  # Command HELP
  if command == '--help':
    commandsFile = open('.json/commands.json', 'r')
    showHelp(loads(commandsFile.read()))
    commandsFile.close()

  # Command INPUT
  elif command == '--input':
    validateMandatoryParameters(['f'], parameters,
      '--input needs parameter -f for the generated input file\'s name')
    generateInputFile(parameters['f'])

  # Command LEARN
  elif command == '--learn':
    validateMandatoryParameters(['i', 'w'], parameters,
      '--learn needs parameters -i and -w to get inputs and save learning')
    constants_file = open('.json/constants.json', 'r')
    constants = loads(constants_file.read())
    constants_file.close()

    (x, d) = readInputFile(parameters['i'])
    alpha = constants['alpha']
    maxError = constants['maxError']
    if 'a' in parameters:
      alpha = float(parameters['a'])
    if 'm' in parameters:
      maxError = float(parameters['m'])

    learningFile = open(parameters['w'], 'w')
    learningFile.write(dumps(learningProcess(x, d, alpha, maxError)))
    learningFile.close()

  # Command RUN
  elif command == '--run':
    validateMandatoryParameters(['w'], parameters,
      '--run needs parameter -o to get learned weights')
    learningFile = open(parameters['w'], 'r')
    (n, m, l, wh, wo) = loads(learningFile.read())
    learningFile.close()

    x2 = []
    if 'o' in parameters:
      x2 = readOutputFile(parameters['o'])
    else:
      x2 = list(product([False, True], repeat=n))

    print '\n'.join([r for r in getY2(x2, n, m, l, wh, wo, True)])


if __name__ == "__main__":
   main(sys.argv[1:])
