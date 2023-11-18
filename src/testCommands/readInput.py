import os
from sympy import symbols, sympify
from sympy.logic.boolalg import to_dnf

def read_equations(file_path):
    equations = []
    arbitrary_variable_counter = 0  # Counter for equations without an output variable
    aribitaryvariable= ['a', 'b', 'c', 'd', 'e', 'f', 'g', 
                        'h', 'i', 'j', 'k', 'l', 'm', 'n', 
                        'o', 'p', 'q', 'r', 's', 't', 'u',
                        'v','w', 'x', 'y', 'z']
    
    base_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(base_name)[0]
    
    with open(file_path, 'r') as file:
        input_variables_line = file.readline().strip()
        output_variables_line = file.readline().strip()

        # Extracting variable names from the lines
        input_variables = input_variables_line.split("inputs: ")[1].split(", ") if "inputs: " in input_variables_line else []
        output_variables = output_variables_line.split("outputs: ")[1].split(", ") if "outputs: " in output_variables_line else []

        for line in file:
            if " = " in line:
                variable, equation = line.strip().split(" = ")
            else:
                # Generate an arbitrary variable name that is not in input or output variables
                while True:
                    variable = f"{aribitaryvariable[arbitrary_variable_counter]}"
                    if variable not in input_variables and variable not in output_variables:
                        break
                    arbitrary_variable_counter += 1

                equation = line.strip()
                arbitrary_variable_counter += 1
            equations.append((variable, equation))
    
    return equations, file_name_without_extension, input_variables, output_variables

def convert_to_canonical(expression, input_variables):
    # Declare the symbols for all input variables
    symbols_dict = {var: symbols(var) for var in input_variables}
    
    # Convert to DNF (Disjunctive Normal Form)
    canonical_expr = to_dnf(expression, simplify=True)
    
    return (str(canonical_expr))

def generate_prime_implicants(minterms):
    # Generate prime implicants from the minterms
    pass

def create_prime_implicant_chart(prime_implicants, minterms):
    # Create the prime implicant chart
    pass

def select_essential_prime_implicants(chart):
    # Select essential prime implicants
    pass

def minimize_remaining_terms(chart, essential_implicants):
    # Find the minimum cover for the remaining terms
    pass

def optimize_equation(equation):
    minterms = convert_to_canonical(equation)
    prime_implicants = generate_prime_implicants(minterms)
    chart = create_prime_implicant_chart(prime_implicants, minterms)
    essential_implicants = select_essential_prime_implicants(chart)
    minimized_expression = minimize_remaining_terms(chart, essential_implicants)
    return minimized_expression

def write_blif(equations, file_name_without_extension, input_variables, output_variables):
    output_file_path = file_name_without_extension + ".blif"
    with open(output_file_path, 'w') as file:
        # Writing input and output variables
        file.write(".model " + file_name_without_extension +'\n')
        file.write(".inputs " + " ".join(input_variables) + '\n')
        file.write(".outputs " + " ".join(output_variables) + '\n')
        
 # Specify the directory path
folder_path = "src/test_examples"

# Get a list of all files in the folder
files = os.listdir(folder_path)
input_file = "src/test_examples/" + "fourInput.txt"  # Replace with your input file path
equations, file_name_without_extension, input_variables, output_variables = read_equations(input_file)
write_blif(equations, file_name_without_extension, input_variables, output_variables)
print(len(equations))
print(equations)
print(equations [0][1])

canonical_expression = convert_to_canonical(equations [0][1], input_variables)
print(canonical_expression)

print("Optimization complete. Check the output file.")