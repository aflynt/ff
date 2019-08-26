#!/opt/rh/rh-python36/root/usr/bin/python
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

csv.register_dialect(\
    'mydialect', delimiter = ',',quotechar = '"', doublequote = True, \
    skipinitialspace = True, lineterminator = '\n' )

def read_file(filename):
  with open(filename, 'r') as f:
    reader = csv.reader(f, delimiter=',')

    # get all the rows as a list
    data = list(reader)

    return data

twoFiles = False

#filename1 = 'names.csv'
#filename1 = 'pos_d.txt'
#filename1 = 'pos_k.txt'
#filename1 = 'pos_qb.txt'
#filename1 = 'pos_rb.txt'
#filename1 = 'pos_te.txt'
filename1 = 'pos_wr.txt'
if len(sys.argv) == 2:
  filename1 = sys.argv[1]
  data = read_file(filename1)
if len(sys.argv) == 3:
  twoFiles = True
  filename1 = sys.argv[1]
  filename2 = sys.argv[2]
  headers, data = read_file(filename1)
  d2 = read_file(filename2)
else:
  data = read_file(filename1)

print("plotting file: " + filename1)

#print(headers)
#print(data.shape)
#ncol=data.shape[1]
#nrow=data.shape[0]
#print(data[:3])

for player in range(len(data)):
  posrank = int(data[player][0])
  allrank = int(data[player][1].rstrip(')').lstrip(' ('))
  name = data[player][2]
  team = data[player][3].rstrip().lstrip()
  price = int(data[player][4].lstrip(' $').rstrip())
  bye = int(data[player][5].lstrip().rstrip())
  if(bye == 11):
    onBoard = False
  else:
    onBoard = True

  if posrank == 73:
    onBoard = False
  data[player][0] = posrank
  data[player][1] = allrank
  data[player][3] = team
  data[player][4] = price
  data[player][5] = bye
  data[player].append(onBoard)
  if not onBoard:
    print(data[player])

def showboard(choice):
  with open('output.dat', 'w') as f:
    for player in reversed(range(len(data))):
      p = data[player]
      if p[0] == choice:
        print("removing player",data[player])
        data[player][-1] = False
        p = data[player]

      # Print player if on board
      if p[-1]:
        f.write('{}\n'.format(p))
        #f.write('\n'.join('{}'.format(p)))

while True:
  choice = input("who to remove?")
  choice = int(choice)
  print("removing #",choice)
  showboard(choice)
