import os

# Change the working directory to the directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

'''
The bitstream is formatted into 8 bit chuncks using ASCII.

Since the file format we are converting to is BLIF, some information can be assumed to save room in the bitstream. There are also
characters that are NEVER used in BLIF files that we are able to use as a delimiter. 

The first three lines of the blif are 
.model
.inputs
.outputs

We use an exclamation mark (!) [00100001] as a delimiter betweeen lines, as it is not used in blif syntax. We can also further minimize the bits needed
to save the header information by using the filename to store the model name.

Our inputs and outputs are only single letters, so each letter can be stored in 8 bits and then a delimiter can be used to signify to go to the next line.

The remaining headers we need to handle are the following:
.names
.end

.names lines will start with an ampersand (&) [00100110]
The lines following the declaration will need to some

Here is an example of how it will be represented:
    .names a b i t
    00- 1
    -01 1
    0-0 1

    [00100110 01100001 01100010 01101001 01110100 00100001] (&abit!)
    [00110000 00110000 00101101 00100000 00110001 00100001] (00- 1!)
    [00101101 00110000 00110001 00100000 00110001 00100001] (00- 1!)
    [00110000 00101101 00110000 00100000 00110001 00100001] (0-0 1!)

.end will be signified with a pound (#) [00100011]

Generate test text here: https://www.rapidtables.com/convert/number/ascii-to-binary.html
'''

def binaryToText(binaryString):
    # Remove spaces from the binary string
    binaryString = binaryString.replace(" ", "")

    # Split the binary string into 8-bit chunks
    eightBitChunks = [binaryString[i:i+8] for i in range(0, len(binaryString), 8)]

    # Convert each 8-bit chunk to decimal and then to ASCII character
    textCharacters = [chr(int(chunk, 2)) for chunk in eightBitChunks]

    # Join the characters to form the final text
    text = ''.join(textCharacters)

    return text

def textToBinaryAscii(textString):
    binary = ""
    for char in textString:
        # Get ASCII value of the character
        asciiValue = ord(char)

        # Convert ASCII value to binary and concatenate to the result
        binary += bin(asciiValue)[2:].zfill(8)  # [2:] removes '0b' prefix, zfill(8) pads with zeros to make it 8 bits

    return binary

def writeToBitstram(filename):
    # Construct the path to the file
    filePath = f"blif/{filename}"

    bitstream = "" # Save a blank bitstream to be written to as the file read occurs

    # Open and read the file one line at a time
    with open(filePath, 'r') as file:
        for line in file:
            # Split the string into a list of words
            words = line.split()

            if words[0] == ".model":
                next
            elif (words[0] == ".inputs" or words[0] == ".outputs"): # this is always the second line
                lineLength = len(words)

                # Loop over the array using a for loop
                for i in range(lineLength):
                    if i == 0:
                        next
                    else:
                        bitstream = bitstream + textToBinaryAscii(words[i])
                bitstream = bitstream + "00100001" # signify end of line
            elif words[0] == ".names":
                bitstream = bitstream + "00100110" # signify end of line
                lineLength = len(words)

                # Loop over the array using a for loop
                for i in range(lineLength):
                    if i == 0:
                        next
                    else:
                        bitstream = bitstream + textToBinaryAscii(words[i])
                bitstream = bitstream + "00100001" # signify end of line
            elif words[0] == ".end":
                bitstream = bitstream + "00100011"
                next
            elif (words[0][0] == "1" or words[0][0] == "0" or words[0][0] == "1" or words[0][0] == "-"): # definition for .names
                bitstream = bitstream + textToBinaryAscii(line.strip())
                bitstream = bitstream + "00100001" # signify end of line
            else:
                next # unsupported BLIF syntax
        
        dotIndex = filename.rfind('.')
        modelName = filename[:dotIndex]

        with open(f'bitstream/{modelName}.txt', 'w') as file:
            file.write(bitstream)

    return 0

def readBitstream(): # returns name of new blif file
    # Specify the directory path
    folderPath = "bitstream"

    # Get a list of all files in the folder
    files = os.listdir(folderPath)

   # Print the list of files
    iter = 0
    print(f"Select a file to use:")
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
    filePath = "bitstream/" + files[fileChoice]
    modelName = files[fileChoice]

    # Open and read the file
    textBitstream = ""
    with open(filePath, 'r') as file:
        contents = file.read()
        textBitstream = binaryToText(contents)

    # Process the bitstream and write to new file
    print(textBitstream)
    with open(f"blif/{modelName[:-4]}.blif", 'w') as file:
        file.write(f'.model {modelName[:-4]}\n')

        # break the bitstream into parts
        bitstreamLines = textBitstream.split("!")
        print(bitstreamLines)

        for index, line in enumerate(bitstreamLines):
            if index == 0: # inputs line
                addSpaces = ' '.join(line)
                file.write(f'.inputs {addSpaces}\n')
            elif index == 1: # outputs line
                addSpaces = ' '.join(line)
                file.write(f'.outputs {addSpaces}\n')
            else:
                if line[0] == '&':
                    addSpaces = ' '.join(line[1:])
                    file.write(f'.names {addSpaces}\n')
                elif line[0] == '#':
                    file.write(f'.end')
                else:
                    file.write(f'{line}\n')

    return f"{modelName[:-4]}.blif"

# default
def main():
    # Example usage:
    # writeToBitstram("aORb.blif")
    readBitstream()

if __name__ == "__main__":
    main()

