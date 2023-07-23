import argparse
parser = argparse.ArgumentParser()
import numpy as np

parser.add_argument('filename')
args = parser.parse_args()
fName = args._get_kwargs()[0][1]


file = open(f'data/{fName}.UXD', 'r')

data = []
for line in file.readlines():    
    while(line[0] == ' '):
        line = line[1:]
    line = line[:len(line)-1]
    
    if(any((line[0] == c for c in ['0','1','2','3','4','5','6','7','8','9','-']))):

        for num in line.split(' '):
            if(num != ''):
                data.append(num)

data = np.reshape(data, (-1,2))

file = open(f'build/{fName}.txt', 'w')
[file.write(f'{d[0]} {d[1]}\n') for d in data]
file.close()