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

    uniqueInputs = []
    for item in inputs:
        if item not in uniqueInputs:
            uniqueInputs.append(item)
    inputs = uniqueInputs

    # Get number of OR clauses and save them
    clauseArray = [] # matrix where each row represents an AND statement
    clauseArray = re.findall(r'[^+]+', booleanFunction[2:]) # Run function on all characters in the input except for the output

    # Get input values (true/false)
    inputBoolArray = booleanArrayFromString(booleanFunction[2:]) # Run function on all characters in the input except for the output

    with open(filename, "a") as file:
        # Append content to the file
        file.write(f".names { ' '.join(inputs + outputs) }")

        # Figure out output for each clause
        for index, clause in enumerate(clauseArray):

            boolInputs = []

            for charIndex, char in enumerate(inputs):
                if char in clauseArray[index]: # If the character appears in the string
                    indexOfChar = clauseArray[index].index(char) 
                    if clauseArray[index][indexOfChar - 1] == '~': # Check if the character before it is a '~'
                        boolInputs.append('0')
                    else:
                        boolInputs.append('1')
                else: # Otherwise don't care
                    boolInputs.append("-")
            
            # Write the result for this loop iter to the file
            outputString = ''.join(map(str, boolInputs))
            file.write(f"\n{outputString} 1")
        file.write(f"\n")

# default
def main():
    booleanFunc = "E=CB~A+aB+~B+A~C"
    filename = "test.txt"

    writeToBLIF(booleanFunc, filename)

if __name__ == "__main__":
    main()