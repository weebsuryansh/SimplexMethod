import pickle
import numpy as np
from typing import List, Tuple
import os

M: float = 999999 #M is a very large number

def next_variable(z: List[float]) -> int:
    max_z = 0
    index = -1

    for ind, i in enumerate(z):
        if i > max_z:
            max_z = i
            index = ind

    return index

def leaving_variable(v: List[float], b: List[float], num_constraints: int) -> int:

    min_ratio: float = M
    index: int = -1

    for i in range(num_constraints):
        if v[i]<=0:
            continue

        ratio: float = b[i]/v[i]
        if ratio <= min_ratio:
            min_ratio = ratio
            index = i

    return index

def gaussian(tableau: List[List[float]], b: List[float], next_var: int, leaving_var: int)-> Tuple[List[List[float]], List[float]]:

    if tableau[next_var][leaving_var] == 0:
        return [[-1]],[-1]

    div_factor: float =1/tableau[next_var][leaving_var]

    for ind, i in enumerate(tableau):
        tableau[ind][leaving_var] = i[leaving_var]*div_factor
    b[leaving_var] = b[leaving_var]*div_factor

    for ind, i in enumerate(b):
        if ind==leaving_var:
            continue
        if tableau[next_var][ind] == 0:
            mul_factor: float = 0
        else:
            mul_factor = tableau[next_var][ind]

        for ind2, j in enumerate(tableau):
            diff = mul_factor*tableau[ind2][leaving_var]
            tableau[ind2][ind] = tableau[ind2][ind] - diff

        b[ind] = i - mul_factor*b[leaving_var]

    return tableau, b

def Simplex(A: List[List[float]], b: List[float], c: List[float]):
    """
    Solve the linear program in standard form:
    
        minimize    c^T x
        subject to  A x = b
                    x >= 0

    Parameters:
    -----------
    A : Matrix
        The coefficient matrix.
    b : Array
        The right-hand side vector.
    c : Array
        The objective function coefficients.
    
    Returns:
    --------
    Tuple of (X, Optimal): any
        Optimal - The optimal solution (or an appropriate result) for the LP.
        X - The solution vector.
        If the problem is infeasible or unbounded, returns a tuple as following:
        (None, 'Infeasible')
    
    Note:
    -----
    You must implement the Simplex algorithm from scratch. The use of inbuilt
    solvers (e.g., from Gurobi, SciPy) is strictly prohibited. You may only use basic
    Python libraries like numpy, pickle, os, etc.
    """

    # converting min problem to max

    b = np.array(b, dtype=float)

    for i in range(len(c)):
        c[i]*=-1

    Optimal: float = 0
    X: List[float] = []
    print("SIMPLEX!")
    z: List[float] = []
    num_variables: int =  len(c)
    num_basic_vectors: int = len(b)
    num_constraints: int = len(b)

    # Initial Tableau
    base_vectors: List[float] = []
    base_vectors_indices: List[int] = []

    for i in range(num_basic_vectors):
        base_vectors.append(-M)
        base_vectors_indices.append(num_variables+i)
        c= np.append(c, -M)

    print(base_vectors_indices)
    print(base_vectors)

    # creating the initial tableau
    tableau: List[List[float]] = []

    for i in range(num_variables):
        temp: List[float] = []
        for j in range(num_constraints):
            temp.append(A[j][i])
        tableau.append(temp)
        print(temp)

    for i in range(num_basic_vectors):
        temp: List[float] = []
        for j in range(num_basic_vectors):
            temp.append(0)
        temp[i] = 1
        tableau.append(temp)
        print(temp)

    print(c)

    #initilising z
    for ind,i in enumerate(tableau):
        sum_temp: float = 0
        for j in range(len(base_vectors)):
            sum_temp+=base_vectors[j]*i[j]
        sum_temp = c[ind]-sum_temp
        z.append(sum_temp)

    print(z)

    next_var: int = next_variable(z)
    print("Next Variable:\t",next_var)


    while next_variable(z)!=-1:
        leaving_var: int = leaving_variable(tableau[next_var], b, num_constraints)
        print("Leaving Variable:\t",leaving_var)

        base_vectors[leaving_var] = c[next_var]
        base_vectors_indices[leaving_var] = next_var
        print(base_vectors)

        tableau, b = gaussian(tableau, b, next_var, leaving_var)
        if b.all() == -1:
            return None, "Infeasible"

        print("tableau")
        for i in tableau:
            print(i)
        print("b")
        print(b)
        for ind,i in enumerate(tableau):
            sum_temp: float = 0
            for j in range(len(base_vectors)):
                sum_temp+=base_vectors[j]*i[j]
            sum_temp = c[ind]-sum_temp
            z[ind] = sum_temp

        print(z)

        next_var: int = next_variable(z)
        print("Next Variable:\t",next_var)


    for i in range(num_variables):
        X.append(0)

    for ind, i in enumerate(base_vectors_indices):
        if i>=num_variables:
            continue
        X[i] = round(b[ind],2)

    for i in range(num_basic_vectors):
        Optimal+= base_vectors[i]*b[i]

    Optimal = -round(Optimal,2)

    print("X\n",X)
    print("Optimal:\t",Optimal)

    return X, Optimal  #Do not change this at all!

def main():
    # DATA LOADING from Input Pickle .pkl file for A, b and c!
    input_filename = 'input_data.pkl'
    try:
        with open(input_filename, 'rb') as f:
            data = pickle.load(f)
    except Exception as e:
        print(f"Error loading input data: {e}")
        return

    A = data['A']
    b = data['b']
    c = data['c']

    # Your Simplex Method is Called here!
    result = Simplex(A, b, c)

    # Output File Creation for Automated Testing!
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    output_filename = script_name + '_solution.pkl'
    with open(output_filename, 'wb') as f:
        pickle.dump(result, f)
    print(f"Solution saved in {output_filename}")

if __name__ == '__main__':
    main()