
def selection_sort(ls):
    for i in range(len(ls)-1):
        min_j = None
        min_val = None
        for j in range(i, len(ls)):
            if min_val == None or ls[j] < min_val:
                min_j = j
                min_val = ls[j]
        ls[i], ls[min_j] = ls[min_j], ls[i]
        print(i, min_j, ls)
    return ls

print(selection_sort([9, 1, 2, 5, 3]))

def binary_search(ls, item):
    '''Assumes ls is a list of numbers sorted increasing '''
    if len(ls) == 1:
        if ls[0] == item:
            return 0
        else:
            raise Exception('Not found')
    midpoint = len(ls)//2
    if ls[midpoint] == item:
        return midpoint
    elif ls[midpoint] < item:
        return midpoint + binary_search(ls[midpoint:], item)
    elif ls[midpoint] > item:
        return binary_search(ls[:midpoint], item)

foo = [1,22]
for x in foo:
    print(binary_search(foo, x))

def fast_insertion_sort(ls):
    for j in range(0, len(ls)):
        key = ls[j]
        i = 0
        for i in range(j-1, -1, -1):
            if ls[i] > key:
                break
            ls[i+1] = ls[i]
        ls[i] = key
    return ls

print(fast_insertion_sort([9, 1, 2, 5, 3]))
