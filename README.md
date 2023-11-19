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

### Logic Synthesis

## Examples
## References