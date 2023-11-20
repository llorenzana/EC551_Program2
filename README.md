# EC551_Program2
#### Leanorine Lorenzana-Garcia & Cole Wentzel

## Table of Contents 
[Overview](#Overview)  
[Organization](#Organization)  
[Functions](#Functions)  
[References](#References)  
[Examples](#Examples)

## Overview
This program creates a virtual FPGA and “connects it” to a logic synthesis function. The program assigns the logic function to “LUTs” on an FGPA and connects those LUTs to realize the function as requested.

The final FPGA is represented as a .blif file.

## Organization
The code is organized into several folders.
`src` is used to hold our main function, as well as our helper functions.
`bitstream` is where bitstream .txt files are saved to and read from.
`blif ` is where BLIF .blif files are saved to and read from.
## Functions
### Bitstream Handling
The bitstream is formatted into 8 bit chuncks using ASCII.

Since the file format we are converting to is BLIF, some information can be assumed to save room in the bitstream. There are also
characters that are *never* used in BLIF files that we are able to use as a delimiter. 

The first three lines of the blif are 
<br/>.model
<br/>.inputs
<br/>.outputs

We use an exclamation mark (!) [00100001] as a delimiter betweeen lines, as it is not used in blif syntax. We can also further minimize the bits needed
to save the header information by using the filename to store the model name.

Our inputs and outputs are only single letters, so each letter can be stored in 8 bits and then a delimiter can be used to signify to go to the next line.

The remaining headers we need to handle are the following:
<br/>.names
<br/>.end

.names lines will start with an ampersand (&) [00100110]
.end will be signified with a pound (#) [00100011]

Here is an example of how a .names can be represented:
    <br/>.names a b i t
    <br/>00- 1
    <br/>-01 1
    <br/>0-0 1

    [00100110 01100001 01100010 01101001 01110100 00100001] (&abit!)
    [00110000 00110000 00101101 00100000 00110001 00100001] (00- 1!)
    [00101101 00110000 00110001 00100000 00110001 00100001] (00- 1!)
    [00110000 00101101 00110000 00100000 00110001 00100001] (0-0 1!)

The functions to handle the bitstream are stored in bitstream.py and commented in detail.
<br/>Here is a brief overview of each function:

<br/>binaryToText(binaryString)
<br/>textToBinaryAscii(textString)
<br/>writeToBitstram(filename)
<br/>readBitstream()

### BLIF Composition
To comprise the BLIF file, we:
1. **File Upload and Access:**
   
    - The user selects a .txt file from the test_cases folder comprised in the following format:

            Number of LUTs: 
            type of LUTs: 
            inputs: 
            outputs:
            <list of boolean equations (i.e. F = A B C)
   
2. **Reading and Parsing Equations:**
    - After reading the file, we parse the equations into a tuple containing on item for the output variable, and one for the Boolean SOP

          num_of_LUT, type_of_LUT, equations, file_name_without_extension, input_variables, output_variables = read_equations(filename)
      
    - Example Output:

            [ ['F' , [A B C + A B D'] , ...] 
3. **Start To Write BLIF File:**
    - From the above, we extract the filename, inputs and outputs and begin to write the top of the .blif file

            startWrite(file_name_without_extension, input_variables, output_variables)

    - Example Output to .blif file:
      
            .model <modelname>
            .inputs <model inputs>
            .outputs <model outputs>
           
4. **Simplify Equations:**
    - from the output of the read_eqautions, we call parse equations which:
        - generates a minimal SOP for all equations and stores them in a list

              simplified = parse_equation(equations)
          
5. **Appending Output Variable to simplified SOP:**
    - If the number of input variables in an SOP, is greater than the number of LUT inputs, it will:
        - sort the SOP into group containing similar inputs
        - assign it an arbitrary output variable (acts as a wire)
        - Function call:  

              simplified, output_list= append_variable(simplified, equations, int(type_of_LUT[0]))
              assigned = assign_inputs(simplified)
          
    - If the function contains wires, combine them using OR to final input:
        - Example, a, b, c represent wires from the broken down equation into F:
                
              F = a + b + c
              
        - Function Call:
      
                final_output_expressions = combine_assigned_inputs(assigned)
           
    - Then it will append the equation to the output variable in the following format:

          F = ABC + BCD
        - Function call:

              final_input = combine_outputs(assigned, output_list)

6. **Combine the Two Sets of Equations to Make One List to Write to .blif:**

       final_input = final_output_expressions + final_input

## Examples
We have written 6 test xamples in the src/test_examples folder:

        1: eightInput_fourLUT.txt
        2: eightInput_sixLUT.txt
        3: fourInput.txt
        4: fourInterdependent.txt
        5: sixInput.txt
        6: sixInterdependent.txt

## References
Programming Assignment 1: https://github.com/llorenzana/EC551_Program1
