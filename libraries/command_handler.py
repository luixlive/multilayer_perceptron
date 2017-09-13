from itertools import product
from json import loads, dumps
from shutil import copyfile
from multilayer_perceptron import learningProcess, getY2

# Constants
CMD_HELP = '--help'
CMD_INPUT = '--input'
CMD_LEARN = '--learn'
CMD_OUTPUT = '--output'
CMD_RUN = '--run'

CONST_ALPHA = 'alpha'
CONST_MAX_ERR = 'maxError'

PARAM_ALPHA = 'a'
PARAM_FILE = 'f'
PARAM_INPUT = 'i'
PARAM_MAX_ERR = 'm'
PARAM_OUTPUT = 'o'
PARAM_ROUND = 'r'
PARAM_SAVE = 's'
PARAM_WEIGHTS = 'w'

# Validate that user's input params have the required ones
def _validateMandatoryParameters(mandatoryParams, inputParams, message):
  for param in mandatoryParams:
    assert param in inputParams, message

# Print all commands in output
def _showHelp(commands):
  print
  for command in commands:
    print '--' + command
    print '\t' + commands[command]['definition']
    print '\t' + 'Params: ' + ', '.join(commands[command]['params'])
    print '\t' + 'Optional params: ' + \
      ', '.join(commands[command]['optionalParams'])
  print

# Copy the template file to the path given
def _generateTemplateFile(template, path):
  copyfile('.templates/' + template, path)

# Generate an input file from the template
def _generateInputFile(path):
  _generateTemplateFile('input_file_template.txt', path)

# Generate an output file from the template
def _generateOutputFile(path):
  _generateTemplateFile('output_file_template.txt', path)

# Transform the input file table format into matrixes 'x' and 'd'
def _extractXD(tableLines):
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
def _extractX2(tableLines):
  x2 = list()
  for row in [l.strip().split(' ') for l in tableLines]:
    x2Temp = list()
    for value in row:
      x2Temp.append(bool(int(value)))
    x2.append(x2Temp)
  return x2

# Read lines of a plain text file with # as comment lines, ignoring empty lines
def _readTableFile(tableFilePath):
  tableFile = open(tableFilePath, 'r')
  table = tableFile.read().splitlines()
  tableFile.close()

  return [l for l in table if len(l.strip()) > 0 and l[0] != '#']

# Read an input file and extract the table into matrixes 'x', 'd' and 'x2'
def _readInputFile(inputFilePath):
  return _extractXD(_readTableFile(inputFilePath))

# Read an output file and extract the table into matrix 'x2'
def _readOutputFile(outputFilePath):
  return _extractX2(_readTableFile(outputFilePath))

# Run command help
def _runCommandHelp(parameters):
  commandsFile = open('.json/commands.json', 'r')
  _showHelp(loads(commandsFile.read()))
  commandsFile.close()

# Run command input
def _runCommandInput(parameters):
  _validateMandatoryParameters([PARAM_FILE], parameters,
    '--input needs parameter -f for the generated input file\'s name')
  _generateInputFile(parameters[PARAM_FILE])

# Run command output
def _runCommandOutput(parameters):
  _validateMandatoryParameters([PARAM_FILE], parameters,
    '--output needs parameter -f for the generated output file\'s name')
  _generateOutputFile(parameters[PARAM_FILE])

# Run command learn
def _runCommandLearn(parameters):
  _validateMandatoryParameters([PARAM_INPUT, PARAM_WEIGHTS], parameters,
    '--learn needs parameters -i and -w to get inputs and save learning')
  constants_file = open('.json/constants.json', 'r')
  constants = loads(constants_file.read())
  constants_file.close()

  (x, d) = _readInputFile(parameters[PARAM_INPUT])
  alpha = constants[CONST_ALPHA]
  maxError = constants[CONST_MAX_ERR]
  if PARAM_ALPHA in parameters:
    alpha = float(parameters[PARAM_ALPHA])
  if PARAM_MAX_ERR in parameters:
    maxError = float(parameters[PARAM_WEIGHTS])

  learningFile = open(parameters[PARAM_WEIGHTS], 'w')
  learningFile.write(dumps(learningProcess(x, d, alpha, maxError)))
  learningFile.close()

# Run command run
def _runCommandRun(parameters):
  _validateMandatoryParameters([PARAM_WEIGHTS], parameters,
    '--run needs parameter -o to get learned weights')
  learningFile = open(parameters[PARAM_WEIGHTS], 'r')
  (n, m, l, wh, wo) = loads(learningFile.read())
  learningFile.close()

  x2 = []
  if PARAM_OUTPUT in parameters:
    x2 = _readOutputFile(parameters[PARAM_OUTPUT])
  else:
    x2 = list(product([False, True], repeat=n))

  results = getY2(x2, n, m, l, wh, wo, PARAM_ROUND in parameters, True)
  resultString = '\n'.join([r for r in results])

  if PARAM_SAVE in parameters:
    learningFile = open(parameters[PARAM_SAVE], 'w')
    learningFile.write('# Requested results running ' + \
      parameters[PARAM_WEIGHTS] + ' network\n')
    learningFile.write(resultString)
    learningFile.close()
  else:
    print resultString

# Map received command with it's function
def runCommand(command, parameters):
  {
    CMD_HELP: _runCommandHelp,
    CMD_INPUT: _runCommandInput,
    CMD_OUTPUT: _runCommandOutput,
    CMD_LEARN: _runCommandLearn,
    CMD_RUN: _runCommandRun
  }[command](parameters)
