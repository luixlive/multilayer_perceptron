import sys
sys.path.append('libraries')
from command_handler import runCommand

# Main function, pass the argv to the command handle
if __name__ == "__main__":
  runCommand(sys.argv[1:]) if len(sys.argv) > 1 else runCommand(['--help'])
