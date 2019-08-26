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

def sort_allrank(val):
  return val[1]

def read_file(filename):
  with open(filename, 'r') as f:
    reader = csv.reader(f, delimiter=',')

    # get all the rows as a list
    data = list(reader)

    for i in range(len(data)):
      data[i].append(filename.rstrip('.txt').lstrip('pos_'))

    return data

twoFiles = False
#filename1 = 'names.csv'
f1 = 'pos_d.txt'
f2 = 'pos_k.txt'
f3 = 'pos_qb.txt'
f4 = 'pos_rb.txt'
f5 = 'pos_te.txt'
f6 = 'pos_wr.txt'
if len(sys.argv) == 2:
  filename1 = sys.argv[1]
  data = read_file(filename1)
if len(sys.argv) == 3:
  twoFiles = True
  filename1 = sys.argv[1]
  filename2 = sys.argv[2]
  data = read_file(filename1)
  d2 = read_file(filename2)
  data = data + d2
else:
  data = read_file(f1)
  d2   = read_file(f2)
  d3   = read_file(f3)
  d4   = read_file(f4)
  d5   = read_file(f5)
  d6   = read_file(f6)
  data = data+d2+d3+d4+d5+d6

# combine positions for all players

# Sort the data based on allrank
data.sort(key = sort_allrank)

# add onBoard Field to player
for player in range(len(data)):
  posrank = int(data[player][0])
  allrank = int(data[player][1].rstrip(') ').lstrip(' ('))
  name = data[player][2]
  team = data[player][3].rstrip().lstrip()
  price = int(data[player][4].lstrip(' $').rstrip())
  bye = int(data[player][5].lstrip().rstrip())
  onBoard = True
  data[player][0] = posrank
  data[player][1] = allrank
  data[player][3] = team
  data[player][4] = price
  data[player][5] = bye
  data[player].append(onBoard)

# show all players on board
def showboard(choice):
  with open('output.dat', 'w') as f:
    for player in reversed(range(len(data))):
      p = data[player]

      # remove player matching choice in allrank
      if p[1] == choice:
        print("removing player",p)
        data[player][-1] = False
        p = data[player]

      # Print player if still on board
      if p[-1]:
        f.write('{}\n'.format(p))
        #f.write('\n'.join('{}'.format(p)))

while True:
  choice = input("who to remove?")
  choice = int(choice)
  print("removing #",choice)
  showboard(choice)
