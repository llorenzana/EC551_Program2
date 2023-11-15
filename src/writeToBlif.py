import os
import re

from blif_to_tt import blif_file_to_tt_file

# Change the working directory to the directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def booleanArrayFromString(inputString):
    result = []

    # Iterate through each character in the input string
    for i in range(len(inputString)):
        # Check if the current character is a variable
        if inputString[i].isalpha():
            # Check if the previous character is a '~'
            if i > 0 and inputString[i - 1] == '~':
                result.append(0)  # ~A becomes False
            else:
                result.append(1)  # A becomes True

    return result

#funcion to add to main.py
def writeToBLIF(booleanFunction, filename):
    '''
    1) get an array with all inputs and array with the output
    2) use + as a delimiter for lines, because each new line is OR'd
    3) for each block of AND variables, check what the variable is and mark it properly on the line
    '''

    print("Running writeToBlif on", booleanFunction)

    # Gets output names
    outputs = ""
    for char in booleanFunction:
        if char == "=":
            break  # Exit the loop when "=" is reached
        outputs += char
    outputs = list(set(outputs))
    
    # Gets input names
    inputs = ""
    inputsBool = []
    for index, char in enumerate(booleanFunction):
        if index >= 2 and char.isalnum(): # Skip the first two characters in the expression because they are the output and the equal
            inputs += (char)
    inputs = list(set(inputs))
    print(inputs)

    # Get number of OR clauses and save them
    clauseArray = [] # matrix where each row represents an AND statement
    clauseArray = re.findall(r'[^+]+', booleanFunction[2:]) # Run function on all characters in the input except for the output
    print(clauseArray)


    # Get input values (true/false)
    inputBoolArray = booleanArrayFromString(booleanFunction[2:]) # Run function on all characters in the input except for the output

    with open(filename, "a") as file:
        # Append content to the file
        file.write(f".names { ' '.join(inputs + outputs) }\n")

# default
def main():
    booleanFunc = "E=CB~A+AB+~B"
    filename = "test.txt"

    writeToBLIF(booleanFunc, filename)

if __name__ == "__main__":
    main()