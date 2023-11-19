from sympy import symbols, sympify
from sympy.logic.boolalg import to_dnf
from itertools import product, combinations

#This function is used to parse and generate minterms based off of the input equations 
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

# number of prime implicants & essential prime implicants
def simplifyExpression (minterms, variables):
    expanded_sum_of_minterms = []
    for minterm in minterms:
        term = "("
        for i, value in enumerate(minterm):
            if value == '0':
                term += f"~{variables[i]} & "
            elif value == '1':
                term += f"{variables[i]} & "
                
        # Remove the trailing "&"
        term = term[:-2]
        expanded_sum_of_minterms.append(term)
    simplified = (") | ".join(expanded_sum_of_minterms) + ")")
    simplified = str(to_dnf(simplified, simplify=True, force=True))
    
    return simplified.replace("(", "").replace(")", "").replace("|", "+").replace("&", "")

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
                        newgroup.remove(term)
                else: 
                    running_vargroup = sorted(list(set(c for term in final_group for c in term if c.isalpha())))
                    if  term_vars not in running_vargroup and (len(running_vargroup) + sum(1 for val in term_vars if val not in running_vargroup)) <= max_inputs:
                        final_group.append(term)
                        newgroup.remove(term)


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

# Example usage (assuming input_variables are known)
expression = " ~A ~B ~C ~D + A ~B ~C ~D + ~B C ~D + B ~C D + B  C  D + ~A B D + F + A B G + B H F + J K L + A H J + J  B  "  # Example Boolean expression
simplified = generateMinterms(expression)
print(simplified)
simplified = split_expression(simplified, 6)
print(simplified)


