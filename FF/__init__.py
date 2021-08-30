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


def clean_player_data(data):
  for player in range(len(data)):
    posrank = int(data[player][0])
    allrank = int(data[player][1].rstrip(') ').lstrip(' ('))
    name    =     data[player][2].strip()
    team    =     data[player][3].strip()
    price   = int(data[player][4].lstrip(' $').rstrip())
    bye     = int(data[player][5].lstrip().rstrip())
    onBoard = True
    data[player][0] = posrank
    data[player][1] = allrank
    data[player][2] = name
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

def showboard(data):
  # show all players on board
  with open('output.dat', 'w') as f:
    for player in reversed(range(len(data))):
      if data[player][-1]:
        ps = print_player(data[player])
        f.write('{}\n'.format(ps))
        #f.write('{}\n'.format(data[player]))
  showpos('d', data)
  showpos('k' , data)
  showpos('qb', data)
  showpos('rb', data)
  showpos('te', data)
  showpos('wr', data)
  plot_player(data)

def picknum(data):
  cnt = 0
  for player in range(len(data)):
    # Print player if still on board
    if not data[player][-1]:
      cnt += 1
  return cnt

# show individual player position list
def showpos(pos, data):
  with open('b_'+pos+'.dat', 'w') as f:
    for player in reversed(range(len(data))):
      p = data[player]

      # Print player if still on board
      if p[-1] and p[-2] == pos:
        ps = print_player(p)
        f.write('{}\n'.format(ps))
        #f.write('{}\n'.format(p))

def find_player(data):
  findname = get_input("Name to Find: ")
  while findname != "done" and findname != '-1':

    findname = findname.lower()
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
def rm_player(data):
  allrank = get_int(get_input("Who to remove?: "))
  while allrank > 0:
    for player in range(len(data)):
      p = data[player]
      if p[1] == allrank:
        data[player][-1] = False
        strpick = 'PICK [%3d], removing player: %s' % (picknum(data), p)
        print(strpick)
    showboard(data)
    allrank = get_int(get_input("Who to remove?: "))

def correct_player(data):
  allrank = get_int(get_input("Who to correct?: "))
  while allrank > 0:
    for player in range(len(data)):
      p = data[player]
      if p[1] == allrank:
        print("correcting player",p)
        data[player][-1] = True
    showboard(data)
    allrank = get_int(get_input("Who to correct?: "))

def indirect(c, data):
  switcher={
      'f':find_player,
      'r':rm_player,
      'c':correct_player,
      'p':plot_player,
      }
  func=switcher.get(c,lambda data :'Invalid')
  return func(data)

def plot_player(data):
  # n = name
  # a = allrank
  # p = posrank
  # t_x = taken
  qb_a = []
  qb_p = []
  wr_a = []
  wr_p = []
  rb_a = []
  rb_p = []
  te_a = []
  te_p = []
  d_a = []
  d_p = []
  k_a = []
  k_p = []
  t_a = []
  t_p = []
  for player in reversed(range(len(data))):
    p = data[player]
    posrank = p[0]
    allrank = p[1]
    pos     = p[6]
    onBoard = p[7]
    if onBoard:
      if pos == 'wr':
        #wr_n.append(pos+'-'+name)
        wr_a.append(allrank)
        wr_p.append(posrank)
      elif pos == 'qb':
        #qb_n.append(pos+'-'+name)
        qb_a.append(allrank)
        qb_p.append(posrank)
      elif pos == 'rb':
        #rb_n.append(pos+'-'+name)
        rb_a.append(allrank)
        rb_p.append(posrank)
      elif pos == 'te':
        #te_n.append(pos+'-'+name)
        te_a.append(allrank)
        te_p.append(posrank)
      elif pos == 'd':
        #d_n.append(pos+'-'+name)
        d_a.append(allrank)
        d_p.append(posrank)
      elif pos == 'k':
        #k_n.append(pos+'-'+name)
        k_a.append(allrank)
        k_p.append(posrank)
    else:
      #t_n.append(pos+'-'+name)
      t_a.append(allrank)
      t_p.append(posrank)


  pick = picknum(data)
  px = [pick,pick]
  py = [0,80]
  fig, ax = plt.subplots()
  line1, = ax.plot(qb_a,qb_p,'b*',label='qb', markersize=4)
  line2, = ax.plot(wr_a,wr_p,'k^',label='wr', markersize=4)
  line3, = ax.plot(rb_a,rb_p,'r+',label='rb', markersize=4)
  line4, = ax.plot(te_a,te_p,'ch',label='te', markersize=4)
  line5, = ax.plot(d_a,d_p,'mx',label='d', markersize=4)
  line6, = ax.plot(k_a,k_p,'go',label='k', markersize=4)
  line7, = ax.plot(t_a,t_p,'y.',label='gone', markersize=2)
  line8, = ax.plot(px,py,'k--',label='pick')
  plt.xlabel('Overall Pick')
  plt.ylabel('Position Rank')
  ax.set_xlim(0,350)
  ax.set_ylim(0,90)
  ax.grid(True)
  ax.legend()
  plt.tight_layout()
  fig.savefig("view_all.png")
  ax.set_xlim(0,100)
  ax.set_ylim(0,60)
  fig.savefig("view_zoom.png")
  plt.close()
  #fig.savefig("test.ps")
  #plt.show()
