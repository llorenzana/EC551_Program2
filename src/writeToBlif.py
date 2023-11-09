import os

from blif_to_tt import blif_file_to_tt_file

# Change the working directory to the directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

#funcion to add to main.py
def writeToBLIF(booleanFunction, filename):
    print("Running writeToBlif on", booleanFunction)

    # Gets output names
    outputs = ""
    for char in booleanFunction:
        if char == "=":
            break  # Exit the loop when "=" is reached
        outputs += char
    
    # Gets input names
    inputs = ""
    for char in booleanFunction:
        if char.isalnum(): # ERROR: finds the initial output
            inputs += char
    print(inputs)

    with open(filename, "a") as file:
        # Append content to the file
        file.write("This is some text in the new file.\n")
        file.write("You can add more lines as needed.")


# default
def main():
    booleanFunc = "C=~A+B"
    filename = "test.txt"

    writeToBLIF(booleanFunc, filename)


if __name__ == "__main__":
    main()