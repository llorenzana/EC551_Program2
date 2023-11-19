import os
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
        num_of_LUT_line = file.readline().strip()
        type_of_LUT_line = file.readline().strip()
        input_variables_line = file.readline().strip()
        output_variables_line = file.readline().strip()
        # Extracting variable names from the lines
        num_of_LUT = num_of_LUT_line.split("Number of LUTs: ")[1].split(" ") if "Number of LUTs: " in num_of_LUT_line else []
        type_of_LUT = type_of_LUT_line.split("type of LUTs: ")[1].split(" ") if "type of LUTs: " in type_of_LUT_line else []
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
    
    return num_of_LUT, type_of_LUT, equations, file_name_without_extension, input_variables, output_variables

def parse_equation(expression):
    simplified = []
    for i in range(len(expression)):
        simple = (generateMinterms(expression[i][1]))
        equation = expression[i][0] + '=' + simple
        simplified.append(equation)
    return simplified

def generateMinterms(expression):
    ##used to find the input variables for the given equation
    operators = {"+"} 
    words = [word.strip() for word in expression.replace('~', ' ').split() if word.strip().isalpha() and word not in operators]
    variables = sorted(list(set(words))) 
     
    # Split the expression at '+' and then strip spaces from each term in boolean equation
    booleanTerm = [minterm.strip() for minterm in expression.split("+")]    
    minterms = []
    
    #for each boolean term in equation find and return the minterms
    for i in range(len(booleanTerm)):   
        binaryterm = mintermToBinary(booleanTerm[i], variables)
        for i in range(len(binaryterm)):
            minterms.append(binaryterm[i])
    minterms = list(set(minterms))
    return simplifyExpression(minterms, variables)

def mintermToBinary(minterm, variables):
    binary = ''
    components = minterm.split()
    for var in variables:
        if var in components:
            binary += '1'
        elif f'~{var}' in components:
            binary += '0'
        else:
            binary += '-' #used in the case of don't cares
    return list(generateCombinations(binary))

#generates the minterms (especially case in which we have don't cares)
def generateCombinations(binary, index=0, combinations=None):
    if combinations is None:
        combinations = set()

    if index == len(binary):
        combinations.add(binary)
        return combinations

    if binary[index] == '-': #returns both cases 
        replaced0 = binary[:index] + '0' + binary[index + 1:]
        replaced1 = binary[:index] + '1' + binary[index + 1:]

        generateCombinations(replaced0, index + 1, combinations)
        generateCombinations(replaced1, index + 1, combinations)
    else:
        generateCombinations(binary, index + 1, combinations)
    return combinations

# takes teh minterms and simplifies them 
def simplifyExpression (minterms, variables):
    expanded_sum_of_minterms = []
    for minterm in minterms:
        term = "("
        for i, value in enumerate(minterm):
            if value == '0':
                term += f"~{variables[i]} & "
            elif value == '1':
                term += f"{variables[i]} & "
        term = term[:-2]
        expanded_sum_of_minterms.append(term)
        
    simplified = (") | ".join(expanded_sum_of_minterms) + ")")
    simplified = str(to_dnf(simplified, simplify=True, force=True))
    return simplified.replace("(", "").replace(")", "").replace("|", "+").replace("&", "").replace(" ", "")

def split_expression(expr, max_inputs):

    # Splits a logic expression into subexpressions, appending expressions with the same first four inputs.
    # Split the expression by '+' to separate OR clauses
    booleanTerm = [minterm.strip() for minterm in expr.split("+")]
    booleanTerm = sorted(booleanTerm, key=len, reverse=True)
    variables = sorted(list(set(c for term in booleanTerm for c in term if c.isalpha())))
    LUT = []

    if max_inputs < len(variables): 
        required_vars = find_required_variables(variables, booleanTerm)
        grouped_terms = []
        unique_terms = []   
        for term in booleanTerm:
            term_vars = set(c for c in term if c.isalpha())
            if term_vars.issuperset(required_vars) and count_unique_variables(term) <= max_inputs:
                running_var = sorted(list(set(c for term in grouped_terms for c in term if c.isalpha())))
                if term_vars not in running_var and (len(running_var) + sum(1 for val in term_vars if val not in running_var)) <= max_inputs:
                    grouped_terms.append(term)
                else:
                    unique_terms.append(term)
            else: 
                unique_terms.append(term)
        
        variablesUnique = sorted(list(set(c for term in unique_terms for c in term if c.isalpha())))
        if max_inputs < len(variablesUnique):  
            #handles teh case of a lot fo inputs    
            newgroup = []
            final_group = []
            required_vars = find_required_variables(variablesUnique, unique_terms)
            for term in unique_terms:
                term_vars = set(c for c in term if c.isalpha())
                if term_vars.issuperset(required_vars) and count_unique_variables(term) <= max_inputs:
                    running_var = sorted(list(set(c for term in newgroup for c in term if c.isalpha())))
                    if  term_vars not in running_var and (len(running_var) + sum(1 for val in term_vars if val not in running_var)) <= max_inputs:
                        newgroup.append(term)
                        unique_terms.remove(term)
                    else: 
                        final_group.append(term)
                        unique_terms.remove(term)
                else: 
                    running_vargroup = sorted(list(set(c for term in final_group for c in term if c.isalpha())))
                    if  term_vars not in running_vargroup and (len(running_vargroup) + sum(1 for val in term_vars if val not in running_vargroup)) <= max_inputs:
                        final_group.append(term)
                        unique_terms.remove(term)


            if newgroup: LUT.append("+".join(newgroup).replace(" ", ""))
            if final_group: LUT.append("+".join(final_group).replace(" ", ""))

        if unique_terms: LUT.append("+".join(unique_terms).replace(" ", ""))
        if grouped_terms: LUT.append("+".join(grouped_terms).replace(" ", ""))
        return list(set(LUT))
    
    else: 
        return expr.replace(" ", "")

def find_required_variables(variables, terms, threshold=0.5):
    # Find variables that appear in a significant number of terms
    var_count = {var: 0 for var in variables}
    for term in terms:
        for var in var_count:
            if var in term:
                var_count[var] += 1

    required_vars = [var for var, count in var_count.items() if count / len(terms) >= threshold]
    return required_vars

def count_unique_variables(term):
    # Count unique variables in a term, ignoring negation symbols
    return len(set(c for c in term if c.isalpha()))


def startWrite(file_name_without_extension, input_variables, output_variables):
    output_file_path = file_name_without_extension + ".blif"
    with open(output_file_path, 'w') as file:
        # Writing input and output variables
        file.write(".model " + file_name_without_extension +'\n')
        file.write(".inputs " + " ".join(input_variables) + '\n')
        file.write(".outputs " + " ".join(output_variables) + '\n')