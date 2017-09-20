from collections import defaultdict

def rev_index(ind, *file):
    for el in file:
        for k in el:
            if file.index(el)+1 not in ind[k]:
                ind[k].append(file.index(el)+1)
    return ind

a = ['Madam', 'I', 'am', 'Adam', 'I']
b = ['Adam', 'love', 'Madam']
c = ['I', 'am', 'bahamamama']
ind = defaultdict(list)
print(rev_index(ind, a, b, c))

