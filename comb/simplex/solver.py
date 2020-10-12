from scipy.optimize import linprog
from random import randint as dice
import time
from collections import defaultdict

def randy():
    '''Generates random numbers for filling A, customized to make them more likely to be solvable'''
    if dice(0,1) == 0:
        return 1
    return dice(-5, 5)

def generate_data(m, n):
    ''' creates problems of the same kind as the example problem, with b and c habing only 1's'''
    A = [[randy() for _ in range(n)] for _ in range(m)]
    b = [[1] for _ in range(m)]
    c = [1 for _ in range(n)]
    return A, b, c

# Result tables
m_n_to_time = defaultdict(list)
m_n_to_tries = defaultdict(int)
m_n_to_matrices = dict()

# parameter space
ns = [4, 10, 20, 30, 40, 50]
ms = [2, 6, 10, 14]

# for each pair of parameters, get 10 successful calculations
for n in ns:
    for m in ms:
        successes = 0
        while successes < 1:
            m_n_to_tries[(m,n)] += 1
            A, b, c = generate_data(m, n)
            tic = time.perf_counter()
            result = linprog(c=c, A_eq=A, b_eq=b, method='simplex')
            toc = time.perf_counter()
            if result['success']:
                m_n_to_time[(m,n)].append(1000*(toc-tic))
                successes += 1
        m_n_to_matrices[(m,n)] = [A,b,c,result['x'], 1000*(toc-tic)]
        print(m, n, result['message'], 
                [int(x) for x in m_n_to_time[(m,n)]], 
                m_n_to_tries[(m,n)])

print()

import pickle
pickle.dump(m_n_to_matrices, open("matrices.pickle", 'wb'))


def make_latex_table(m_n_to_str):
    print('\\begin{tabular}[c|cccc]')
    print('n, m &' + ' & '.join([str(m) for m in ms]) + '\\\\')
    print('\\hline')
    for n in ns:
        print(n, end=' & ')
        for m in ms:
            print(m_n_to_str(m, n), end='')
            if m != ms[-1]:
                print(' & ', end='')
        if n != ns[-1]:
            print(' \\\\')
        else:
            print()
    print('\\end{tabular}')

def avg(ls):
    return sum(ls)/len(ls)
make_latex_table(lambda m, n : round(avg(m_n_to_time[(m,n)]), 3))
make_latex_table(lambda m, n : m_n_to_tries[(m,n)])
