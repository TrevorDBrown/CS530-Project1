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
    languageCharacters = []
    stateTransitions = []
    currentState = ""

    # Constructor
    def __init__(self):
        self.faStates = []
        self.languageCharacters = []
        self.stateTransitions = []
        self.currentState = ""
    
    def addState(self, newState):
        self.faStates.append(newState)
    
    def findState(self, stateID):
        for state in (self.faStates):
            if (state.id == stateID):
                return state
        
        return ""

    def addLanguageCharacter(self, newLanguageCharacter):
        self.languageCharacters.append(newLanguageCharacter)

    # checkWord - checks the entire user input to see if it is a valid word in the language defined by the FA.
    def checkWord(self, word):
        self.currentState = ""

        for faState in self.faStates:
            if (faState.id == "A"):
                self.currentState = faState

        for i, character in enumerate(word):
            if (isinstance(self.currentState, str)):
                print("currentState variable test failed. Tested as string.")
                return False
            else:
                goodTransition, nextState = self.currentState.checkTransition(character)

                if (goodTransition):
                    self.stateTransitions.append(self.currentState)
                    self.currentState = nextState

                    if (i >= len(word) - 1):
                        self.stateTransitions.append(self.currentState) 

                else:
                    print("A bad transition occurred.")
                    return False

        # Print the transitions.
        self.printTransitions(word)

        # Print if the word is valid or invalid.
        if (self.currentState.isFinalState):
            print("The word, %s, is valid." % (word))
            return True

        else:
            print("The word, %s, is invalid." % (word))
            return False

    # print - Prints the Machine and all of its states.
    def print(self):
        print("The FA Machine:")

        for faState in self.faStates:

            if (faState.isFinalState):
                print("(%s):" % (faState.id), end=" ")
            else:
                print(" %s :" % (faState.id), end=" ")
            
            for faConnection in faState.connections:
                if (faConnection.isFinalState):
                    print("(%s)" % (faConnection.id), end=" ")
                else:
                    print(" %s " % (faConnection.id), end=" ")

            print("")
    
    # printTransitions - prints the transitions taken thus far, or overall, when processing an input.
    def printTransitions(self, word):
        print("Transition Graph for %s: " % (word))

        for i, state in enumerate(self.stateTransitions):
            if (state.isFinalState):
                print("(%s)" % (state.id), end=" ")
            else:
                print("%s" % (state.id), end=" ")

            if (i < len(self.stateTransitions) - 1):
                print("-- %s -->" % (word[i]), end=" ")
            else:
                print("") # for the new line

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

    def addConnection (self, transitionValue, newState):
        self.connections.append({"nextState": newState, "transitionValue": transitionValue})
    
    # checkTransition - checks if the specified input can get from the current state to the next state.
    def checkTransition(self, input):
        try:
            nextState = self.connections[int(input)]
            return True, nextState

        except:
            print("Unable to transition to next state.")
            return False, self
    
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

# readFAFile - reads the specified file, parsing its content for FA states and final states.
def readFAFile(filename, faMachine):
    dimensionsCollected = False
    acceptFAStates = True
    finalStatesCollected = False
    finalStateSet = False

    stateIDs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    maxX = 0
    maxY = 0
    currentY = 0
    finalStatesCount = 0

    try:
        with open(filename) as f:
            for line in f:
                # Split line content, remove new line characters
                currentLine = line.replace("\n", "").split(" ")

                # Determine if line is dimensional value or actual value.
                if (not dimensionsCollected):
                    dimensionsCollected = True

                    maxX = int(currentLine[0])
                    maxY = int(currentLine[1])

                    for x in range(maxX):
                        newState = FAState(stateIDs[x])
                        faMachine.addState(newState)
                    
                    for y in range(maxY):
                        faMachine.addLanguageCharacter(y)

                else:
                    try:
                        firstCharacterIntTest = int(currentLine[0])
                        acceptFAStates = False
                        finalStatesCount = currentLine[0]
                    except:
                        if ((type(currentLine[0]) != "int") and (acceptFAStates)):
                            currentFAState = faMachine.findState(stateIDs[currentY])

                            if (currentFAState == ""):
                                print("Error - state does not exist.")
                            else:
                                for connectionID in currentLine:
                                    connectionState = faMachine.findState(connectionID)

                                    if (connectionState == ""):
                                        print("Error - state does not exist for specified connection.")
                                    else:
                                        currentFAState.connections.append(connectionState)
                        
                            currentY += 1

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
    except:
        print("Unable to read FA file.")
        return ""

    return faMachine

# main - main function of the script.
def main():
    
    # Create blank FA
    faMachine = FA()

    # Retrieve filename
    faFilename = input("What is the name of the file containing the FA file? ")

    # Read file content
    faMachine = readFAFile(faFilename, faMachine)

    if (faMachine != ""):
        # Print the FA 
        faMachine.print()

        # Retrieve word
        word = input("What word would you like to test against the FA? ")

        if (word != ""):
            # Validate the Word
            faMachine.checkWord(word)

# Calling main...
main()