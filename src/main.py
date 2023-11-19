import os

from utilis import read_equations, parse_equation, append_variable, assign_inputs, combine_assigned_inputs, combine_outputs, startWrite, call_write
from bitstream import writeToBitstream, readBitstream

# Change the working directory to the directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# default
def main():
    
    print("Welcome to our EDA TOOL! \n")
    print("Would you like to: " )
    print("1. Load a bitstream")
    print("2. Read input from a file")
    choice = input("Enter 1 or 2: ")
    
    if choice == '1': 
        loadedFilename = readBitstream()
        print(f"Loaded bitstream to blif/{loadedFilename}.")
    elif choice == '2': 
        ### IF LOAD FROM FILE INPUT IS CHOSEN
        # Specify the directory path
        folderPath = "test_examples"

        # Get a list of all files in the folder
        files = os.listdir(folderPath)

    # Print the list of files
        iter = 0
        print(f"\nSelect a file to use:")
        for index, file in enumerate(files):
            print(f"{index + 1}: {file}")

        # Get and error check user choice (DOES NOT CHECK IF FILE IS BLIF)
        while True:
            fileChoice = int(input("Enter your selection: "))

            #Error check user choice
            fileChoice = fileChoice - 1 #Set choice to python indexing

            if (fileChoice >= 0 and fileChoice < len(files)):
                break
            else:
                print("Please select a valid file.")

        #process filename selection
        filename = "test_examples/" + files[fileChoice]
        
        num_of_LUT, type_of_LUT, equations, file_name_without_extension, input_variables, output_variables = read_equations(filename)
        startWrite(file_name_without_extension, input_variables, output_variables)
        simplified = parse_equation(equations)
        simplified, output_list= append_variable(simplified, equations, int(type_of_LUT[0]))
        assigned = assign_inputs(simplified)
        final_output_expressions = combine_assigned_inputs(assigned)
        final_input = combine_outputs(assigned, output_list)
        final_input = final_output_expressions + final_input
        final_input = final_input[1:]
        call_write(final_input, int(num_of_LUT[0]), file_name_without_extension)
        writeToBitstream(file_name_without_extension + ".blif")
        print(f"Logic mapping written to blif/{file_name_without_extension}.blif")       
        
    else: 
        print("Invalid choice. Please enter '1' or '2'.")
    
if __name__ == "__main__":
    main()