#!/opt/rh/rh-python36/root/usr/bin/python
import sys
import csv
import matplotlib.pyplot as plt

csv.register_dialect(\
    'mydialect', delimiter = ',',quotechar = '"', doublequote = True, \
    skipinitialspace = True, lineterminator = '\n' )

def get_input(str):
  try:
    val = input(str)
  except EOFError as verr:
    val = '-1'
  return val

def get_int(val):
  try:
    ival = int(val)
  except ValueError as verr:
    ival = -1
  return ival

def sort_allrank(val):
  return val[1]

def read_file(filename):
  with open(filename, 'r') as f:
    reader = csv.reader(f, delimiter=',')

    # get all the rows as a list
    data = list(reader)

    # append position to data
    for i in range(len(data)):
      data[i].append(filename.rstrip('.txt').lstrip('pos_'))

    return data

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

def print_player(p):
  posrank = p[0]
  allrank = p[1]
  name    = p[2]
  team    = p[3]
  price   = p[4]
  bye     = p[5]
  pos     = p[6]
  onBoard = p[7]
  ps = '%2s %2d %3d %3s |%20s| bye=%2d' % (pos, posrank, allrank, team, name, bye)
  #print(ps)
  return ps

def showboard():
  # show all players on board
  with open('output.dat', 'w') as f:
    for player in reversed(range(len(data))):
      if data[player][-1]:
        ps = print_player(data[player])
        f.write('{}\n'.format(ps))
        #f.write('{}\n'.format(data[player]))
  showpos('d')
  showpos('k')
  showpos('qb')
  showpos('rb')
  showpos('te')
  showpos('wr')

# show individual player position list
def showpos(pos):
  with open('b_'+pos+'.dat', 'w') as f:
    for player in reversed(range(len(data))):
      p = data[player]

      # Print player if still on board
      if p[-1] and p[-2] == pos:
        ps = print_player(p)
        f.write('{}\n'.format(ps))
        #f.write('{}\n'.format(p))

def find_player():
  findname = get_input("Name to Find: ")
  while findname != "done" and findname != '-1':
    for player in reversed(range(len(data))):
      p = data[player]
      pname = p[2].lower()
      hasName = pname.find(findname)

      # Print player if has name
      if hasName != -1:
        ps = print_player(p)
        print(ps)
        #print_player(p)
    findname = get_input("Name to Find: ")


# remove player matching choice in allrank
def rm_player():
  allrank = get_int(get_input("Who to remove?: "))
  while allrank > 0:
    for player in range(len(data)):
      p = data[player]
      if p[1] == allrank:
        print("removing player",p)
        data[player][-1] = False
    showboard()
    allrank = get_int(get_input("Who to remove?: "))

def correct_player():
  allrank = get_int(get_input("Who to correct?: "))
  while allrank > 0:
    for player in range(len(data)):
      p = data[player]
      if p[1] == allrank:
        print("correcting player",p)
        data[player][-1] = True
    showboard()
    allrank = get_int(get_input("Who to correct?: "))

def indirect(c):
  switcher={
      'f':find_player,
      'r':rm_player,
      'c':correct_player,
      }
  func=switcher.get(c,lambda :'Invalid')
  return func()

if __name__ == "__main__":
  while True:
    print(''' Pick action:
          f == find player
          r == remove player
          c == correct player status
          ''')
    pick = get_input("Choice: ")
    indirect(pick)
    showboard()
