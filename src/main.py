import os
from blif_to_tt import blif_file_to_tt_file
from utilis import read_equations, parse_equation, startWrite

# Change the working directory to the directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# default
def main():
    print("Main function placeholder.")

if __name__ == "__main__":
    main()