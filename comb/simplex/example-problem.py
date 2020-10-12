import pickle
import numpy as np
import array_to_latex as a2l
import time
#n=4, m=2
A = [[1,2,-1,-1],
     [-1,-5,2,3]]
b = [[1],[1]]
c = [1,1,1,1]
from scipy.optimize import linprog
tic = time.perf_counter()
result = linprog(c=c, A_eq=A, b_eq=b, method='simplex')
toc = time.perf_counter()
print(result)
x = result['x']
for name, code in [
        ('A', 
            lambda: a2l.to_ltx(np.array(A), frmt = '{}', arraytype = 'bmatrix')),
        ('b^T',
            lambda: a2l.to_ltx(np.array(b).T, frmt = '{}', arraytype = 'bmatrix')),
        ('c',
            lambda: a2l.to_ltx(np.array(c), frmt = '{}', arraytype = 'bmatrix')),
        ('x^T',
            lambda: a2l.to_ltx(np.array(x), frmt = '{:3.2}', arraytype = 'bmatrix'))]:
    print()
    print(f'$ {name} =')
    code()
    print('$')
    print()
print()
print(1000*(toc-tic), ' ms')
print()
