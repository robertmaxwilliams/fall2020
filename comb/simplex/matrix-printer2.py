
import pickle
import numpy as np
np.set_printoptions(linewidth=120)
m_n_to_matrices = pickle.load(open("matrices.pickle", 'rb'))
import array_to_latex as a2l
A = np.array([[1.23456, 23.45678],[456.23, 8.239521]])

# parameter space
ns = [4, 10, 20, 30, 40, 50]
ms = [2, 6, 10, 14]

for n in ns:
    for m in ms:
        A, b, c, x, runtime = m_n_to_matrices[(m,n)]
        print(f'\nProblem instance for m={m}, n={n}')
        print('A =')
        print(np.array(A))
        print('b^T =')
        print(np.array(b).T)
        print('c =')
        print(np.array(c))
        print('x^T =')
        print(np.array(x))
        print(f'runtime = {runtime:3.3} ms')
