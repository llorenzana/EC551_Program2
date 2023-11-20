import os
from sympy.logic.boolalg import to_dnf
from writeToBlif import writeToBLIF

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
            equations.append([variable, equation])
    
    return num_of_LUT, type_of_LUT, equations, file_name_without_extension, input_variables, output_variables

def parse_equation(expression):
    simplified = []
    for i in range(len(expression)):
        simple = (generateMinterms(expression[i][1]))
        simplified.append(simple)
    return simplified
#This function is used to parse and generate minterms based off of the input equations 
def generateMinterms(expression):
    ##used to find the input variables for the given equation
    operators = {"+"} 
    variables = sorted(set(c for term in expression for c in term if c.isalpha()))
     
    # Split the expression at '+' and then strip spaces from each term in boolean equation
    booleanTerm = [minterm.strip() for minterm in expression.split("+")]    
    minterms = []
    
    #for each boolean term in equation find and return the minterms
    for i in range(len(booleanTerm)):   
        binaryterm = mintermToBinary(booleanTerm[i], variables)
        for i in range(len(binaryterm)):
            minterms.append(binaryterm[i])
    minterms = list(set(minterms))
    
    return simplifyExpression([int(minterm, 2) for minterm in minterms], variables)

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

def simplifyExpression(mt, variables):
    def mul(x,y): # Multiply 2 minterms
        res = []
        for i in x:
            if i+"'" in y or (len(i)==2 and i[0] in y):
                return []
            else:
                res.append(i)
        for i in y:
            if i not in res:
                res.append(i)
        return res

    def multiply(x,y): # Multiply 2 expressions
        res = []
        for i in x:
            for j in y:
                tmp = mul(i,j)
                res.append(tmp) if len(tmp) != 0 else None
        return res

    def refine(my_list,dc_list): # Removes don't care terms from a given list and returns refined list
        res = []
        for i in my_list:
            if int(i) not in dc_list:
                res.append(i)
        return res

    def findEPI(x): # Function to find essential prime implicants from prime implicants chart
        res = []
        for i in x:
            if len(x[i]) == 1:
                res.append(x[i][0]) if x[i][0] not in res else None
        return res

    def findVariables(pi): # Function to find variables in a meanterm. For example, the minterm --01 has C' and D as variables
        # Map the binary representation in the prime implicant to the corresponding variables
        result = []
        for i, char in enumerate(pi):
            if char == '1':
                result.append(variables[i])
            elif char == '0':
                result.append(f'~{variables[i]}')
        return result

    def flatten(x): # Flattens a list
        flattened_items = []
        for i in x:
            flattened_items.extend(x[i])
        return flattened_items

    def findminterms(a): #Function for finding out which minterms are merged. For example, 10-1 is obtained by merging 9(1001) and 11(1011)
        gaps = a.count('-')
        if gaps == 0:
            return [str(int(a,2))]
        x = [bin(i)[2:].zfill(gaps) for i in range(pow(2,gaps))]
        temp = []
        for i in range(pow(2,gaps)):
            temp2,ind = a[:],-1
            for j in x[0]:
                if ind != -1:
                    ind = ind+temp2[ind+1:].find('-')+1
                else:
                    ind = temp2[ind+1:].find('-')
                temp2 = temp2[:ind]+j+temp2[ind+1:]
            temp.append(str(int(temp2,2)))
            x.pop(0)
        return temp

    def compare(a,b): # Function for checking if 2 minterms differ by 1 bit only
        c = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                mismatch_index = i
                c += 1
                if c>1:
                    return (False,None)
        return (True,mismatch_index)

    def removeTerms(_chart,terms): # Removes minterms which are already covered from chart
        for i in terms:
            for j in findminterms(i):
                try:
                    del _chart[j]
                except KeyError:
                    pass
                
    dc = []
    mt.sort()
    minterms = mt
    size = len(bin(minterms[-1]))-2
    groups,all_pi = {},set()

    # Primary grouping starts
    for minterm in minterms:
        try:
            groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(size))
        except KeyError:
            groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(size)]
    # Primary grouping ends


    # Process for creating tables and finding prime implicants starts
    while True:
        tmp = groups.copy()
        groups,m,marked,should_stop = {},0,set(),True
        l = sorted(list(tmp.keys()))
        for i in range(len(l)-1):
            for j in tmp[l[i]]: # Loop which iterates through current group elements
                for k in tmp[l[i+1]]: # Loop which iterates through next group elements
                    res = compare(j,k) # Compare the minterms
                    if res[0]: # If the minterms differ by 1 bit only
                        try:
                            groups[m].append(j[:res[1]]+'-'+j[res[1]+1:]) if j[:res[1]]+'-'+j[res[1]+1:] not in groups[m] else None # Put a '-' in the changing bit and add it to corresponding group
                        except KeyError:
                            groups[m] = [j[:res[1]]+'-'+j[res[1]+1:]] # If the group doesn't exist, create the group at first and then put a '-' in the changing bit and add it to the newly created group
                        should_stop = False
                        marked.add(j) # Mark element j
                        marked.add(k) # Mark element k
            m += 1
        local_unmarked = set(flatten(tmp)).difference(marked) # Unmarked elements of each table
        all_pi = all_pi.union(local_unmarked) # Adding Prime Implicants to global list
        if should_stop: # If the minterms cannot be combined further
            break
    
    # Process for creating tables and finding prime implicants ends


    sz = len(str(mt[-1])) # The number of digits of the largest minterm
    chart = {}
    for i in all_pi:
        merged_minterms,y = findminterms(i),0
        for j in refine(merged_minterms,dc):
            x = mt.index(int(j))*(sz+1) # The position where we should put 'X'
            y = x+sz
            try:
                chart[j].append(i) if i not in chart[j] else None # Add minterm in chart
            except KeyError:
                chart[j] = [i]

    EPI = findEPI(chart) # Finding essential prime implicants
    removeTerms(chart,EPI) # Remove EPI related columns from chart

    if(len(chart) == 0): # If no minterms remain after removing EPI related columns
        final_result = [findVariables(i) for i in EPI] # Final result with only EPIs
    else: # Else follow Petrick's method for further simplification
        P = [[findVariables(j, ) for j in chart[i]] for i in chart]
        while len(P)>1: # Keep multiplying until we get the SOP form of P
            P[1] = multiply(P[0],P[1])
            P.pop(0)
        final_result = [min(P[0],key=len)] # Choosing the term with minimum variables from P
        final_result.extend(findVariables(i) for i in EPI) # Adding the EPIs to final solution
    return (' + ' .join(''.join(i) for i in final_result))

# number of prime implicants & essential prime implicants
def split_expression(expr, max_inputs):
    # Splits a logic expression into subexpressions based on the number of inputs allowed
    # Split the expression by '+' to separate OR clauses
    terms = [minterm.strip() for minterm in expr.split("+")]
    terms = sorted(terms, key=len, reverse=True)
    variables = sorted(set(c for term in terms for c in term if c.isalpha()))

    if len(variables) <= max_inputs:
        return [expr.replace(" ", "")]

    required_vars = find_required_variables(variables, terms)
    grouped_terms, remaining_terms = group_terms(terms, required_vars, max_inputs)

    LUT = []
    if grouped_terms:
        LUT.append("+".join(grouped_terms).replace(" ", ""))
    if remaining_terms:
        LUT.extend(split_remaining_terms(remaining_terms, max_inputs))

    return list(set(LUT))

def find_required_variables(variables, terms, threshold=0.5):
    # Find variables that appear in a significant number of terms
    var_count = {var: 0 for var in variables}
    for term in terms:
        for var in var_count:
            if var in term:
                var_count[var] += 1

    return [var for var, count in var_count.items() if count / len(terms) >= threshold]

def count_unique_variables(term):
    # Count unique variables in a term, ignoring negation symbols
    return len(set(c for c in term if c.isalpha()))

def group_terms(terms, required_vars, max_inputs):
    # Group terms based on the number of inputs and required variables
    grouped_terms = []
    remaining_terms = []
    for term in terms:
        term_vars = set(c for c in term if c.isalpha())
        if term_vars.issuperset(required_vars) and count_unique_variables(term) <= max_inputs:
            grouped_terms.append(term)
        else:
            remaining_terms.append(term)
    return grouped_terms, remaining_terms

def split_remaining_terms(terms, max_inputs):
    # Further split the remaining terms into subexpressions based on max inputs
    subexpressions = []
    current_group = []
    for term in terms:
        if count_unique_variables(term) <= max_inputs:
            if current_group and count_unique_variables("".join(current_group + [term])) > max_inputs:
                subexpressions.append("+".join(current_group).replace(" ", ""))
                current_group = [term]
            else:
                current_group.append(term)
        else:
            if current_group:
                subexpressions.append("+".join(current_group).replace(" ", ""))
                current_group = []
            subexpressions.append(term.replace(" ", ""))

    if current_group:
        subexpressions.append("+".join(current_group).replace(" ", ""))

    return subexpressions

def append_variable(expr, equations, max_input ):
    equation_parse = []
    output_list = []
    for i in range(len(expr)):
        equation_parse.append(split_expression(str(expr[i]), max_input))
        output_list.append(equations[i][0])
    return equation_parse, output_list

def assign_inputs(expressions):
    """
    Assigns an arbitrary input to each expression in the nested list,
    unless the group contains only one expression.
    Returns a nested list of tuples with the original expression and its assigned input or the expression itself.
    """
    arbitrary_variable_counter = 0  # Counter for equations without an output variable
    aribitaryvariable= ['a', 'b', 'c', 'd', 'e', 'f', 'g', 
                        'h', 'i', 'j', 'k', 'l', 'm', 'n', 
                        'o', 'p', 'q', 'r', 's', 't', 'u',
                        'v','w', 'x', 'y', 'z']
    assigned_all = []
    for group in expressions:
        if len(group) == 1:
            assigned_all.append([(group[0], group[0])])
        else:
            # Assign arbitrary inputs to expressions
            assigned_group = []
            for expr in group:
                arbit = aribitaryvariable[0]
                assigned_input = f"{arbit}"
                aribitaryvariable.remove(arbit)
                assigned_group.append([assigned_input, expr])
            assigned_all.append(assigned_group)
    return assigned_all

def combine_outputs(assigned_expressions, final_output_vars):
    """
    Combines the outputs of the assigned expressions using logical OR, and assigns them to the final output variable.
    Returns a single expression representing the final output.
    """
    combined_outputs = []
    for group, output_var in zip(assigned_expressions, final_output_vars):
        if len(group) == 1:
            combined_expression = f"{output_var} = {group[0][1]}"
        else:
            # Combine assigned inputs
            combined_expression = f"{output_var} = " + " + ".join([assigned[0] for assigned in group])
        combined_outputs.append(combined_expression)
    return combined_outputs

def combine_assigned_inputs(assigned_inputs):
    formatted_expressions = []
    for expr in assigned_inputs[0]:  # considering only the first sublist
        formatted_expression = f"{expr[0]} = {expr[1]}"
        formatted_expressions.append(formatted_expression)
    return formatted_expressions


def startWrite(file_name_without_extension, input_variables, output_variables):
    output_file_path = file_name_without_extension + ".blif"
    with open(f"blif/{output_file_path}", 'w') as file:
        # Writing input and output variables
        file.write(".model " + file_name_without_extension +'\n')
        file.write(".inputs " + " ".join(input_variables) + '\n')
        file.write(".outputs " + " ".join(output_variables) + '\n')
        
def call_write(final_input, num_LUTs, filename):
    output_file_path = filename + ".blif"
    for i in range(len(final_input)):
        if num_LUTs < len(final_input):
            return "LUT mapping Not Possible"
        else:
            writeToBLIF(final_input[i], output_file_path)
            
    with open(f"blif/{output_file_path}", 'a') as file:
        file.write(".end")
        
    return ".blif write complete"