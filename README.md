# Database-Normal-Form-Checker
Given a table and its functional dependencies, check if the table is in 2NF, 3NF and BCNF.

## Input format
The tool reads data from standard input. I suggest you put the data in a file and pass the file as input to the program. For an example, see the input file.

## Output
The program will print out candidate keys, prime attributes, non-prime attributes, 2NF information, 3NF information, and BCNF information. The program will print out one of the functional dependencies which breaks the requirements for either 2NF, 3NF, or BCNF, if such a dependency is found.

## Running the checker
python3 ./checker.py < input
