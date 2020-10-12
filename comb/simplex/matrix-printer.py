import pickle
import numpy as np
m_n_to_matrices = pickle.load(open("matrices.pickle", 'rb'))
import array_to_latex as a2l
A = np.array([[1.23456, 23.45678],[456.23, 8.239521]])

# parameter space
ns = [4, 10, 20, 30, 40, 50]
ms = [2, 6, 10, 14]

print('''\documentclass[8pt]{article}
    % General document formatting
    \\usepackage[margin=0.7in]{geometry}
    \\usepackage[parfill]{parskip}
    \\usepackage[utf8]{inputenc}
    
    % Related to math
    \\usepackage{amsmath,amssymb,amsfonts,amsthm,etoolbox}
    \\setcounter{MaxMatrixCols}{50}

    \\def\\env@bmatrix{\\hskip -\\arraycolsep
      \\let\\@ifnextchar\\new@ifnextchar
      \\array{*\\c@MaxMatrixCols r}}

\\AtBeginEnvironment{bmatrix}{\\setlength{\\arraycolsep}{2pt}}
  
    
    \\begin{document}\n''')

for n in ns:
    for m in ms:
        print()
        print('\\section{', f'm={m}, n={n}', '}\n')
        print()
        A, b, c, x, runtime = m_n_to_matrices[(m,n)]
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
            if n == 30:
                print('\\small')
            if n == 40:
                print('\\tiny')
            if n == 50:
                print('\\tiny')
            print(f'$ {name} =')
            code()
            print('$')
            print()
        print()
        print(runtime, ' ms')
        print()

print('''\\end{document}''')
