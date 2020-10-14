# finite-automata-process.py - the main file of the project.
# By - Trevor D. Brown
# In partial fulfillment of credit for CS 530 (Automata Theory and Compiler Construction), taught by Dr. Mustafa Atici at Western Kentucky University, Fall 2020 semester.
#
# Purpose - reads in a file containing data on a Deterministic Finite Automata (DFA) and accepts user input.
#           User input is defined as words containing characters "0-9"
#           The DFA file is formatted as follows:
#               x y                 (how many rows and columns are expected in the file. Each row is assigned an alpha character (A-Z), while columns are assigned 0-9)
#               A B C D ... ⍺^x     (each row contains a listing of state names (A-Z))
#               B C D E ... ⍺^x
#               ...
#               ⍺^y ⍺^y ⍺^y ⍺^y ... ⍺^x
#               z                   (the number of final states)
#               A B C ... ⍺^z        (the listing of final states (A-Z))
#
#           In reality, this script does not utilize the numbers in the file. It does this based on data read in. However, validations can be put in to utilize 
#           the values, to ensure that the data provided is what is expected.

# Imports
import os   # Used for reading the FA file.
import sys  # Used for reading arguments from the command line (if we want to process a filename and input word from the command)

# Finite Automata (FA) - the class that stores the states in our FA machine.
class FA:
    # Attributes
    faStates = []               # faStates - FAState instances within the FA
    languageCharacters = []     # languageCharacters - valid characters in our proprosed language
    stateTransitions = []       # stateTransitions - for a given input, which states were traversed. The first state appened to the list is always state A.
    currentState = ""           # currentState - the FAState we're currently at during traversal. 

    # Constructor
    def __init__(self):
        self.faStates = []
        self.languageCharacters = []
        self.stateTransitions = []
        self.currentState = ""
    
    # addState - adds a specified state (newState) to the specified FA (faStates)
    def addState(self, newState):
        self.faStates.append(newState)
    
    # findState - searches the specified FA's faStates list for the specified next state (string representing the state's ID). 
    #             returns the requested FAState if found
    #             returns an empty ID if an FAState is not found.
    def findState(self, stateID):
        for state in (self.faStates):
            if (state.id == stateID):
                return state
        
        return ""

    # addLanguageCharacter - adds a character to the list of possible characters in the specified FA
    def addLanguageCharacter(self, newLanguageCharacter):
        self.languageCharacters.append(newLanguageCharacter)

    # checkWord - checks the entire user input to see if it is a valid word in the language defined by the FA.
    def checkWord(self, word):
        self.currentState = ""

        # Search faStates for the current FA for FAState with ID "A"
        for faState in self.faStates:
            if (faState.id == "A"):
                self.currentState = faState

        # For each character in the word, check the traversal of the FA via the specified word.
        for i, character in enumerate(word):
            # If the currentState is a string, then an error occurred while processing a nextState. End processing.
            if (isinstance(self.currentState, str)):
                return False
            else:
                # If the currentState is an FAState (i.e. not a string), then call checkTransition with the current character to find the next state.
                goodTransition, nextState = self.currentState.checkTransition(character)

                # If a transition is found, append the list of transitions, and store the next state as the current state.
                if (goodTransition):
                    self.stateTransitions.append(self.currentState)
                    self.currentState = nextState

                    # If we've reached the end of the word, store the current state in the list of state transitions.
                    if (i >= len(word) - 1):
                        self.stateTransitions.append(self.currentState) 

                else:
                    # If no transition is found, throw an error and stop processing.
                    print("An invalid transition occurred.")
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
        # Of course, it has to have a title...
        print("The FA Machine:")
        
        # Print the language characters at the top of the printing
        for x in self.languageCharacters:
            if (x == 0):
                print("     ", end=" ")

            if (x < len(self.languageCharacters) - 1):
                print("%i  " % (x), end=" ")
            else:
                print("%i" % (x))

        # Loop through all faStates, printing its ID, and the IDs of all state transitions
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

        # For each state in the stateTransitions list, print the character which reached the state, and the state's ID.
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
    # Attributes
    id = ''                     # id - a string representing a unique identifier for the FAState.
    connections = []            # connections - a list of FAStates that are connected to the current FAState.
    isFinalState = False        # isFinalState - a boolean flag which indicates if the current state is a final state in the FA.

    # Constructor
    def __init__(self, id):
        self.id = id
        self.connections = []
        self.isFinalState = False

    # addConnection - adds an FAState and transition value to the connections list, to indicate the connection to a new FAState. 
    def addConnection (self, transitionValue, newState):
        self.connections.append({"nextState": newState, "transitionValue": transitionValue})
    
    # checkTransition - checks if the specified input can get from the current state to the next state.
    #                   returns boolean representing a good transition, and the next FAState being access.
    #                   if the check fails, values returned are False and the current FAState.
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
    # Processing variables
    dimensionsCollected = False             # dimensionsCollected - boolean flag that indicates if the dimension information at the top of the input file has been read. This is set to True after the first line is read.
    acceptFAStates = True                   # acceptFAStates - boolean flag that indicates if the read process is accepting FAState and connections listings. Tis is ste to False once the next integer is reached (count of final states)
    finalStatesCollected = False            # finalStatesCollected - boolean flag that indicates if the final states have been processed yet. 
    finalStateSet = False                   # finalStateSet - boolean flag which indicates that a specified final state was found in the list of FAStates for the specified FA. If it remains false after parsing the list, then the FAState doesn't exist.

    stateIDs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"     # stateIDs - a listing of all possible state IDs. Our assumption regarding the FAState IDs and the input language would suggest single alpha characters for FAState IDs and 0-9 numeric characters for characters in the language.

    maxX = 0                    # maxX - the first value read in the file. Indicates the number of characters in the language. If larger than 9, an error should be thrown.
    maxY = 0                    # maxY - the second value read in the file. Indicates the number of FAStates in the FA. If larger than 26, an error should be thrown.
    currentY = 0                # currentY - indicates which FAState we're currently on.
    finalStatesCount = 0        # finalStatesCount - the last numeric value read from the file. Indicates the number of final states to expect.

    # Attempt to read the specified file. Throw an error, if the file is not found or if something happens during the read process.
    try:
        with open(filename) as f:
            for line in f:
                # Split line content, remove new line characters
                currentLine = line.replace("\n", "").strip().split(" ")

                # Determine if line is dimensional value or actual value.
                # If the dimensional line, store its values.
                if (not dimensionsCollected):
                    dimensionsCollected = True

                    maxX = int(currentLine[0])
                    maxY = int(currentLine[1])

                    # For the range of 0 to maxX, store a numeric.
                    
                    if ((1 <= maxX) and (maxX <= 10)):
                        for x in range(maxX):
                            faMachine.addLanguageCharacter(x)
                    else:
                        print("Error - unable to define characters for language. Value must be between 1 and 10. Value currently set to %i." % (maxX))
                        return ""

                    if ((1 <= maxY) and (maxY <= 26)):
                        for y in range(maxY):
                            newState = FAState(stateIDs[y])
                            faMachine.addState(newState)
                    else:
                        print("Error - unable to define states for FA. Value must be between 1 and 26. Value currently set to %i." % (maxY))
                        return ""

                else:
                    # Assume we're already at the final states count.
                    # If the first character won't convert to an int, we know we're still processing states.
                    # If the first character will convert to an int, we can assume we're ready to process final states.
                    try:
                        firstCharacterIntTest = int(currentLine[0])
                        # If it can reach here, then we know it's a valid numeric value, thus ending the input 
                        acceptFAStates = False
                        finalStatesCount = firstCharacterIntTest

                        if (currentY != maxY):
                            print("Error - mismatch between number of states promised, and number of states provided. %i (actual)/%i (promised)" % (currentY, maxY))
                            return ""

                    except:
                        # If we're currently accepting FA states...
                        if (acceptFAStates):
                            currentFAState = faMachine.findState(stateIDs[currentY])

                            if (currentFAState == ""):
                                print("Error - state does not exist.")
                                return ""
                            else:
                                if (maxX == len(currentLine)):
                                    for connectionID in currentLine:
                                        connectionState = faMachine.findState(connectionID)

                                        if (connectionState == ""):
                                            print("Error - state does not exist for specified connection.")
                                            return ""
                                        else:
                                            currentFAState.connections.append(connectionState)
                                else:
                                    print("Error - mismatch between number of connections promised, and number of connections provided. State %s: %i (actual)/%i (promised)" % (stateIDs[currentY], len(currentLine), maxX))
                                    return ""
                        
                            currentY += 1

                        elif ((not acceptFAStates) and (not finalStatesCollected)):
                            if (finalStatesCount != len(currentLine)):
                                print("Error - mismatch between number of final states promised, and number of final states read. %i (actual)/%i (promised)" % (len(currentLine), finalStatesCount))
                                return ""

                            else:
                                for finalState in currentLine:
                                    finalStateSet = False

                                    for machineState in faMachine.faStates:
                                        if (machineState.id == finalState):
                                            machineState.isFinalState = True
                                            finalStateSet = True
                                    
                                    if (not finalStateSet):
                                        print("Error: Specified Final State does not exist in machine.")
                                        return ""

            f.close()
    except Exception as e:
        # A general exception. Regardless, the file can't be read.
        print("Error attempting to read FA file.")
        print(e)
        return ""

    return faMachine

# extractArgs - if arguments are provided, we determine what those arguments are for, and if they are valid.
def extractArgs():
    filename = ""
    word = ""

    # Parse through any provided arguments to determine if 
    for i, arg in enumerate(sys.argv):
        if (i != 0):
            if ((arg == '--help') or (arg == '-h')):
                print("Help")
                print("-f, --file: the filename of a FA file.")
                print("-h, --help: this help guide.")
                print("-w, --word: the input word to test.")
                print("The program will ask for a filename and word, if either or are not provided.")
                exit()
            elif ((arg == '--file') or (arg == '-f')):
                filename = sys.argv[i + 1]
            elif ((arg == '--word') or (arg == '-w')):
                word = sys.argv[i + 1]

    return filename, word

# main - main function of the script.
def main():
    # Check command arguments to determine if filename and/or input have been provided
    faFilename, word = extractArgs()

    # Create blank FA
    faMachine = FA()

    # Retrieve filename
    if (faFilename == ""):
        faFilename = input("What is the name of the file containing the FA file? ")

    # Read file content
    faMachine = readFAFile(faFilename, faMachine)

    if (faMachine != ""):
        # Print the FA 
        faMachine.print()

        # Retrieve word
        if (word == ""):
            word = input("What word would you like to test against the FA? ")

        # If the word is not returned as a empty string...
        if (word != ""):
            # Validate the Word
            faMachine.checkWord(word)

# Calling the driver...
main()