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
    
    return simplified.replace("(", "").replace(")", "").replace("|", "+").replace("&", "").replace(" ", "")


# Example usage (assuming input_variables are known)
expression = " ~A ~B ~C ~D + A ~B ~C ~D + ~B C ~D + B ~C D + B  C  D + ~A B D "  # Example Boolean expression

simplified = generateMinterms(expression)
print(simplified)

