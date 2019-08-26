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
  allrank = data[player][1]
  name = data[player][2]
  team = data[player][3]
  price = data[player][4]
  bye = data[player][5]
  # print(data[data[player]][6])
  # print('player: ',name,'has ranks: ',posrank,allrank,' on team ',team,' and costs:',price)
  print(posrank,allrank,price,team,name)
#01, (043) , Patrick Mahomes   , KC  , $18,  12 

#plot the data
#for i in range(1,ncol):
  #plt.plot(data[:,0], data[:,i], label=headers[i])

#if twoFiles:
#  ncol=d2.shape[1]
#  for i in range(1,ncol):
#    plt.plot(d2[:,0], d2[:,i], '--', label=h2[i])


# curve smoothing
#for i in range(1,ncol):
#  fi = savgol_filter(data[:,i], 51, 3) # window size 51, polynomial order 3
#  plt.plot(data[:,0], fi, label=headers[i]+'-fit')

#plt.xlabel('Time (s)')
#plt.ylabel(headers[1])
#plt.xlim(1.1,2.1)
#plt.xticks([1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1])
#plt.grid(True)
#plt.legend()
##plt.savefig('latest.png')
#ofile = filename1.replace("csv", "png")
#ofile = ofile.replace("dat", "png")
#plt.savefig(ofile)
#plt.show()
print(" ")

"""
# SAVE DATA TO FILE
#with open('output.dat', 'w') as f:
#  f.write('\n'.join('{} {} {}'.format(t[0], t[1], t[2]) for t in zip(r0, r1, f1)))
#  f.close()

# MANUAL PLOTTING
#plt.ylim(-4,4)
plt.ylabel(r'$Forces$ $(N)$')
plt.title('Global Forces')
plt.plot(r0,r1  ,'-', label=r'$F_x (N)$')
plt.plot(r0,r2  ,'-', label=r'$F_y (N)$')
plt.plot(r0,r3  ,'-', label=r'$F_z (N)$')
"""
