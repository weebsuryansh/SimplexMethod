# Simplex Method
This mini-project implements **Simplex Tableau** method to solve **Linear Programming Problem**.
The program expects LPP in **standard form**:
```
        minimize    c^T x
        subject to  A x = b
                    x >= 0
```
I have implemented **Big M Tableau** variation of **Simplex method** which first converts the 
minimization problem into a maximization problem and then introduces artificial variables
a<sub>i</sub> or A<sub>i</sub> with penalty M which is assumed to be a very large integer.

## Tech Details
- Project is completely implemented in python
- Program takes input from `input_data.pkl`
- Program outputs the solution in `code_2022519_solution.pkl`

## Project Structure
```
SimplexMethod/ 
├── code_2022519.py             # Main code file
├── code_2022519_solution.pkl   # Output file 
├── correct_solution.pkl        # File containing correct solution 
├── input_data.pkl              # Input file 
└── Tester.py                   # Python code to test the output
```