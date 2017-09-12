from collections import defaultdict

def indexing(ind, *file):
    for el in file:
        for k in el:
            ind[k].append(file.index(el)+1)
    return ind

def tokenize(file):
    f = open(file, 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    text = text.replace('\n', ' ')
    text = text.split(' ')
    for a in text:
        a = a.strip('.,!?')
    return(text)

def work(files):
    tokens = []
    for a in files:
        tokens.append(tokenize(a))
    #print(tokens)
    return tokens

a = ['Madam', 'I', 'am', 'Adam', 'I']
b = ['Adam', 'love', 'Madam']
c = ['I', 'Am', 'bahamamama']
files = ['1.txt', '2.txt', '3.txt']
ind = defaultdict(list)
print(tokenize('1.txt'))
print(indexing(ind, a, b, c))
#print(indexing(ind, work(files)))

