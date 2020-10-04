# finite-automata-process.py - the main file of the project.
# By - Trevor D. Brown
# In partial fulfillment of credit for CS 530 (Automata Theory and Compiler Construction), taught by Dr. Mustafa Atici at Western Kentucky University, Fall 2020 semester.
#
# Purpose - reads in a file containing data on a Deterministic Finite Automata (DFA) and accepts user input.
#           User input is defined as words containing characters "0-9"
#           The DFA file is formatted as follows:
#               x y                 (how many rows and columns are expected in the file. Each row is assigned an alpha character (A-Z), while columns are assigned 0-9)
#               A B C D ... x       (each row contains a listing of state names (A-Z))
#               B C D E ... x
#               ...
#               y y y y ... x
#               z                   (the number of final states)
#               A B C ... z         (the listing of final states (A-Z))
#
#           In reality, this script does not utilize the numbers in the file. It does this based on data read in. However, validations can be put in to utilize 
#           the values, to ensure that the data provided is what is expected.

# Imports
import os   # Used for reading the FA file.

# Finite Automata (FA) - the class that stores the states in our FA machine.
class FA:
    faStates = []

    # Constructor
    def __init__(self):
        self.faStates = []

    # print - Prints the Machine and all of its states.
    def print(self):
        print("The FA Machine:")

        for faState in self.faStates:
            print("%s:" % (faState.id), end=" ")
            
            for faConnection in faState.connections:
                print("%s" % (faConnection), end=" ")
            
            if (faState.isFinalState):
                print("(Final State)", end=" ")

            print("")

# FA State - the class that stores the ID, the "Final State" flag, and the listing of connections to other states.
class FAState:
    id = ''
    connections = []
    isFinalState = False

    # Constructor
    def __init__(self, id):
        self.id = id
        self.connections = []
        self.isFinalState = False
    
    # print - Prints the state's information.
    def print(self):
        print("Node: %s" % (self.id))
        print("Connections: ", end=" ")

        for i, connection in enumerate(self.connections):
            if (i < len(self.connections) - 1):
                print("%s " % (connection), end=" ")
            else:
                print("%s" % (connection))
            
        print("Final State: " % (self.isFinalState))

# UserInput - class that represents the user's provided input, and the state transitions that occur during processing.
class UserInput:
    value = ''
    stateTransitions = []

    # Constructor
    def __init__(self, input):
        self.value = input
        self.stateTransitions = []
    
    # printInput - prints the user's specified input.
    def printInput(self):
        print("Input: %s" % (self.value))

    # printTransitions - prints the transitions taken thus far, or overall, when processing an input.
    def printTransitions(self):
        for i, state in enumerate(self.stateTransitions):
            print("%s" % (state), end=" ")

            if (i < len(self.stateTransitions) - 1):
                print("--%s-->" % (self.value[i]), end=" ")
            else:
                print("") # for the new line

# readFAFile - reads the specified file, parsing its content for FA states and final states.
def readFAFile(filename):
    dimensionsCollected = False
    acceptFAStates = True
    finalStatesCollected = False
    finalStateSet = False

    nodeIDs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    faMachine = FA()
    faMatrixX = 0
    faMatrixY = 0
    currentY = 0
    finalStatesCount = 0

    with open(filename) as f:
        for line in f:
            # Split line content, remove new line characters
            currentLine = line.replace("\n", "").split(" ")

            # Determine if line is dimensional value or actual value.
            if (not dimensionsCollected):
                dimensionsCollected = True
                faMatrixX = currentLine[0]
                faMatrixY = currentLine[1]
            else:
                try:
                    firstCharacterIntTest = int(currentLine[0])
                    acceptFAStates = False
                    finalStatesCount = currentLine[0]
                except:
                    if ((type(currentLine[0]) != "int") and (acceptFAStates)):
                        newFAState = FAState(nodeIDs[currentY])
                        
                        for nodeID in currentLine:
                            newFAState.connections.append(nodeID)
                    
                        currentY += 1

                        faMachine.faStates.append(newFAState)

                    elif ((not acceptFAStates) and (not finalStatesCollected)):
                        for finalState in currentLine:
                            finalStateSet = False

                            for machineState in faMachine.faStates:
                                if (machineState.id == finalState):
                                    machineState.isFinalState = True
                                    finalStateSet = True
                            
                            if (not finalStateSet):
                                print("Error: Specified Final State does not exist in machine.")
                        
    
        f.close()

    return faMachine

# checkTransition - checks if the specified input can get from the current state to the next state.
def checkTransition(input, currentState, faNode):
    try:
        nextState = faNode.connections[int(input)]
        return True, nextState
    except:
        print("Unable to transition to next state.")
        return False, ""

# checkInput - checks the entire user input to see if it is a valid word in the language defined by the FA.
def checkInput(input, faMachine):
    currentState = "A"

    for i, character in enumerate(input.value):
        currentNode = ""

        for faState in faMachine.faStates:
            if (faState.id == currentState):
                currentNode = faState

        if (isinstance(currentNode, str)):
            return False
        else:
            goodTransition, nextState = checkTransition(character, currentState, currentNode)
            
            if (goodTransition):
                input.stateTransitions.append(currentState)
                currentState = nextState

                if (i >= len(input.value) - 1):
                   input.stateTransitions.append(currentState) 

            else:
                print("A bad transition occurred.")
                return False

    for faState in faMachine.faStates: 
        if (faState.id == currentState):
            if (faState.isFinalState):
                return True
            else:
                return False
    
    return False

# main - main function of the script.
def main():
    # Variable Declaration
    userInput = ''

    # Retrieve filename
    faFilename = input("What is the name of the file containing the FA file? ")

    # Read file content
    faMachine = readFAFile(faFilename)

    # Print the FA 
    faMachine.print()

    # Retrieve word
    word = input("What word would you like to test against the FA? ")
    
    # Initialize the UserInput
    userInput = UserInput(word)

    # Validate the Word
    validWord = checkInput(userInput, faMachine)
    
    # Print the transitions.
    userInput.printTransitions()
    
    # Print wether or not the word is valid/invalid.
    if (validWord):
        print("The word, %s, is valid." % (userInput.value))
    else:
        print("The word, %s, is invalid." % (userInput.value))

# Calling main...
main()