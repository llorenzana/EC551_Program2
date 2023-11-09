import os
from blif_to_tt import blif_file_to_tt_file

# Change the working directory to the directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

#funcion to add to main.py
def writeToBLIF(booleanFunction):
    print("Running writeToBlif on", booleanFunction)

# default
def main():
    booleanFunc = "C=~A+B"
    writeToBLIF(booleanFunc)


if __name__ == "__main__":
    main()