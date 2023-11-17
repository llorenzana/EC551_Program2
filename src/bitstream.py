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

We use an exclamation mark as a delimiter betweeen lines, as it is not used in blif syntax. We can also further minimize the bits needed
to save the header information by using the filename to store the model name.

Our inputs and outputs are only single letters, so each letter can be stored in 8 bits and then a delimiter can be used to signify to go to the next line.

The remaining headers we need to handle are the following:
.names
.end
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

def writeToBitstram(filename):
    # Construct the path to the file
    filePath = f"blif/{filename}"

    bitstream = "" # Save a blank bitstream to be written to as the file read occurs

    # Open and read the file one line at a time
    with open(filePath, 'r') as file:
        for line in file:
            # Process each line as needed
            print(line.strip())  # Strip removes the newline character at the end of each line

    return 0

def readBitstream():
    # Specify the directory path
    folder_path = "blif"

    # Get a list of all files in the folder
    files = os.listdir(folder_path)

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
    return 0

# default
def main():
    # Example usage:
    binaryString = "01001000 01100101 01101100 01101100 01101111"  # Example: "HELLO" in binary
    textResult = binaryToText(binaryString)
    
    print("Binary:", binaryString)
    print("Text:", textResult)

    writeToBitstram("aAndB.blif")

if __name__ == "__main__":
    main()

