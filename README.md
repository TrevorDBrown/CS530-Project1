# CS530-Project1
An implementation of a Deterministic Finite Automata (DFA) constructor and interpreter. Written for CS 530 (Automata Theory and Compiler Construction), Fall 2020 semester, Western Kentucky University.

## Motivation
This project is designed to read in a file of a specified format, which contains a definition of a Deterministic Finite Automata (DFA). From there, the file is interpreted, and determined to be valid or invalid. A word, or input, is accepted, and processed through the DFA. Finally, once parsed, it is determined to be a valid or invalid word.

## Technical Requirements
In order to run the script as intended, you must have Python 3 installed. No additional modules are required.

## Installation
To install and run this application:
1. Install Python 3
2. Clone this repository to your local machine
3. Run python3 ./finite-automata-processor.py

## Usage
A few flags are available upon execution, to bypass direct input into the application on run.

**-f (or --file)** - the filename of your DFA file.
**-h (or --help)** - a listing of these flags.
**-w (or --word)** - the input word to test against the DFA.

If no flags are specified, prompts are given for the needed input.

## DFA File Format
The DFA file is a simple text document, which follows the format:

*x* *y* 
A B C ... (*alpha*)<sup>*x*</sup>
A B C ... (*alpha*)<sup>*x*</sup>
...
(*alpha*)<sup>*y*</sup>
z
A B C ... (*alpha*)<sup>*z*</sup>

*x* and *y* are integers which define the grid size of the DFA. The range of *x* and *y* are 1 <= x <= 10 (representative of language characters), and 1 <= y <= 26 (representative of DFA State IDs), respectively. Language characters are defined as 0-9, and the DFA state IDs are A-Z. 

Examples of these files can be seen in the repository as input.txt and input2.txt.

## Word Format
Words are constructed from valid language characters for a specified DFA. To determine which characters are valid for a language, check the defined *x* value (see DFA File Format), and subtract 1. From there, the language characters are 0 to x - 1.

For the sample files provided, input.txt's valid language characters are 0-2, and input2.txt's valid language characters are the entire range (0-9).

## Output
Once a valid DFA file is read, and a valid input is provided, you will be presented with the following output in the Terminal:

The FA Machine:
     0  1  2  ... 9
A    A  B  C  ... J
B    B  C  D  ... K
C    C  D  E  ... L
...
(Z)    (Z)  A  B  ... I

Transition Graph for (*input word*):
A -- (*character 0*) --> B -- (*character 1*) --> C ... -- (*character n*) --> (Z)
The word, (*input word*), is valid/invalid.

If a DFA State ID is surrounded by parenthesis, it is a final state. A word is deemed valid if it ends on a final state, and invalid otherwise (i.e. ends on non-final state, an invalid transition occurs, etc.)