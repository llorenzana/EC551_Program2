import os
from utilis import read_equations, parse_equation, append_variable, assign_inputs, combine_assigned_inputs, combine_outputs, startWrite, call_write

# Change the working directory to the directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# default
def main():
    print("Welcome to our EDA TOOL! \n")
    print("Would you like to: \n" )
    print("1. Input a bitstream \n")
    print("2. Read from a file \n")
    choice = input("Enter 1 or 2: ")
    
    if choice == '1': 
        pass
    elif choice == '2': 
        filename = "test_examples/" + "fourInput.txt" 
        num_of_LUT, type_of_LUT, equations, file_name_without_extension, input_variables, output_variables = read_equations(filename)
        startWrite(file_name_without_extension, input_variables, output_variables)
        simplified = parse_equation(equations)
        simplified, output_list= append_variable(simplified, equations, int(type_of_LUT[0]))
        assigned = assign_inputs(simplified)
        final_output_expressions = combine_assigned_inputs(assigned)
        final_input = combine_outputs(assigned, output_list)
        final_input = final_output_expressions + final_input
        call_write(final_input, int(num_of_LUT[0]), file_name_without_extension)
    else: 
        print("Invalid choice. Please enter '1' or '2'.")
    
if __name__ == "__main__":
    main()