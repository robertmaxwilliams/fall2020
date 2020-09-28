thread_entry(Int p):
    Int total = 0

    for i from 0 to 7:
        total += A[8*p+i]
    # Partial sums stored at 0 8 16 24 | 32 40 48 56
    A[8*p] = total

    if p >= 4:
        halt()
    # Partial sums stored at 0 8 16 24
    A[8*p] += A[8*p + 32]

    if p >= 2:
        halt()
    # Partial sums stored at 0 8 
    A[8*p] += A[8*p + 16]
    
    if p == 1:
        halt()
    # Final sum stored at 0 
    A[0] += A[8]
    halt()



