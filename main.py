import sys
sys.path.append('libraries')

from command_handler import runCommand

# Capture dynamic parameters
def getDynamicParameters(parameters):
  parametersDict = dict()
  for k, v in [p.split('=') if '=' in p else [p, True] for p in parameters]:
    assert k[0] == '-', 'ERROR: Wrong param ' + k
    parametersDict[k[1:]] = v
  return parametersDict

# Main function, receives the input arguments and determines the code to run
def main(argv):
  if len(argv) == 0:
    argv.append('--help')

  command = argv[0]
  parameters = dict()
  if len(argv) > 1:
    parameters = getDynamicParameters(argv[1:])

  runCommand(command, parameters)

# Map main function
if __name__ == "__main__":
   main(sys.argv[1:])
