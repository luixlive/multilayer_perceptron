from itertools import product
from json import loads, dumps
from shutil import copyfile
from multilayer_perceptron import learningProcess, getY2

# Constants
COMMAND_HELP = '--help'
COMMAND_INPUT = '--input'
COMMAND_OUTPUT = '--output'
COMMAND_LEARN = '--learn'
COMMAND_RUN = '--run'

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
  _validateMandatoryParameters(['f'], parameters,
    '--input needs parameter -f for the generated input file\'s name')
  _generateInputFile(parameters['f'])

# Run command output
def _runCommandOutput(parameters):
  _validateMandatoryParameters(['f'], parameters,
    '--output needs parameter -f for the generated output file\'s name')
  _generateOutputFile(parameters['f'])

# Run command learn
def _runCommandLearn(parameters):
  _validateMandatoryParameters(['i', 'w'], parameters,
    '--learn needs parameters -i and -w to get inputs and save learning')
  constants_file = open('.json/constants.json', 'r')
  constants = loads(constants_file.read())
  constants_file.close()

  (x, d) = _readInputFile(parameters['i'])
  alpha = constants['alpha']
  maxError = constants['maxError']
  if 'a' in parameters:
    alpha = float(parameters['a'])
  if 'm' in parameters:
    maxError = float(parameters['m'])

  learningFile = open(parameters['w'], 'w')
  learningFile.write(dumps(learningProcess(x, d, alpha, maxError)))
  learningFile.close()

# Run command run
def _runCommandRun(parameters):
  _validateMandatoryParameters(['w'], parameters,
    '--run needs parameter -o to get learned weights')
  learningFile = open(parameters['w'], 'r')
  (n, m, l, wh, wo) = loads(learningFile.read())
  learningFile.close()

  x2 = []
  if 'o' in parameters:
    x2 = _readOutputFile(parameters['o'])
  else:
    x2 = list(product([False, True], repeat=n))

  results = '\n'.join([r for r in getY2(x2, n, m, l, wh, wo, True)])

  if 's' in parameters:
    learningFile = open(parameters['s'], 'w')
    learningFile.write('# Requested results running ' + parameters['w'] + \
      ' network\n')
    learningFile.write(results)
    learningFile.close()
  else:
    print results

# Map received command with it's function
def runCommand(command, parameters):
  {
    COMMAND_HELP: _runCommandHelp,
    COMMAND_INPUT: _runCommandInput,
    COMMAND_OUTPUT: _runCommandOutput,
    COMMAND_LEARN: _runCommandLearn,
    COMMAND_RUN: _runCommandRun
  }[command](parameters)
