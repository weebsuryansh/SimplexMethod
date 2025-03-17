import sys
import pickle
import numpy as np

def main():
    if len(sys.argv) != 2:
        print("Usage: python tester.py <student_solution_file>")
        sys.exit(1)
    student_file = sys.argv[1]
    try:
        with open('correct_solution.pkl', 'rb') as f:
            correct = pickle.load(f)
    except Exception as e:
        print("Error loading correct_solution.pkl:", e)
        sys.exit(1)
    try:
        with open(student_file, 'rb') as f:
            student = pickle.load(f)
    except Exception as e:
        print("Error loading student solution file:", e)
        sys.exit(1)
    if (not isinstance(correct, tuple)) or (len(correct) != 2):
        print("Correct solution file format is incorrect.")
        sys.exit(1)
    if (not isinstance(student, tuple)) or (len(student) != 2):
        print("Student solution file format is incorrect.")
        sys.exit(1)
    correct_opt, correct_x = correct
    student_opt, student_x = student
    tol = 1e-6
    if np.isscalar(correct_opt) and np.isscalar(student_opt):
        try:
            correct_num = float(correct_opt)
            student_num = float(student_opt)
        except Exception as e:
            print("Error converting optimal values to float:", e)
            sys.exit(1)
        if np.abs(correct_num - student_num) < tol and np.allclose(correct_x, student_x, atol=tol):
            print("Test passed: Student solution is correct.")
        else:
            print("Test failed: Student solution does not match the correct solution.")
            print("Correct solution:", correct)
            print("Student solution:", student)
    elif isinstance(correct_opt, str) or isinstance(student_opt, str):
        if correct_opt == student_opt:
            if (correct_x is None and student_x is None) or (
                isinstance(correct_x, (list, np.ndarray)) and isinstance(student_x, (list, np.ndarray)) and np.allclose(correct_x, student_x, atol=tol)
            ):
                print("Test passed: Student solution is correct.")
            else:
                print("Test failed: Student solution does not match the correct solution.")
                print("Correct solution:", correct)
                print("Student solution:", student)
        else:
            print("Test failed: Student solution does not match the correct solution.")
            print("Correct solution:", correct)
            print("Student solution:", student)
    else:
        if np.allclose(correct_opt, student_opt, atol=tol) and np.allclose(correct_x, student_x, atol=tol):
            print("Test passed: Student solution is correct.")
        else:
            print("Test failed: Student solution does not match the correct solution.")
            print("Correct solution:", correct)
            print("Student solution:", student)
if __name__ == '__main__':
    main()