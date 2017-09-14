import sys
sys.path.append('libraries')

from command_handler import runCommand

# Main function, pass the argv to the command handle
def main(argv):
  runCommand(argv) if len(argv) > 0 else runCommand(['--help'])

# Map main function
if __name__ == "__main__":
   main(sys.argv[1:])
