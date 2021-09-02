import csv
import matplotlib.pyplot as plt
import json
from operator import contains, itemgetter
from colorama import Fore, Back, Style
from enum import Enum
from draft_order import get_pick_numbers

class Color(Enum):
    OFF    = 1
    GOOD   = 2
    DELIM  = 3
    PROMPT = 4
    CHILL = 5
    RESET = 6
    POS_WR = 7
    POS_TE = 8
    POS_K  = 9
    POS_QB = 10
    POS_RB = 11
    POS_D  = 12

def get_list_of_players(fname):
    with open(fname) as f:
        plist = json.load(f)
    
    for p in plist:
        p['onBoard'] = True

    return plist

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

def color_wrap(ps, inColor):
    e = Style.RESET_ALL
    f = b = s = Style.RESET_ALL

    if inColor == Color.OFF:
        f = Fore.LIGHTRED_EX
        b = Back.BLACK
        s = Style.DIM
    elif inColor == Color.GOOD:
        f = Fore.YELLOW
        #b = Back.RESET
        b = Back.BLUE
        s = Style.BRIGHT
    elif inColor == Color.PROMPT:
        f = Fore.RED
        b = Back.RESET
        s = Style.BRIGHT
    elif inColor == Color.DELIM:
        f = Fore.BLACK
        b = Back.WHITE
        s = Style.NORMAL
    elif inColor == Color.CHILL:
        f = Fore.MAGENTA
        b = Back.RESET
        s = Style.NORMAL
    elif inColor == Color.RESET:
        f = Fore.RESET
        b = Back.RESET
        s = Style.RESET_ALL
    elif inColor == Color.POS_WR: # YELLOW BLUE
        f = Fore.YELLOW
        b = Back.BLUE
        s = Style.BRIGHT
    elif inColor == Color.POS_TE: # B M
        f = Fore.BLACK
        b = Back.MAGENTA
        s = Style.NORMAL
    elif inColor == Color.POS_K:
        f = Fore.RED
        b = Back.RESET
        s = Style.NORMAL
    elif inColor == Color.POS_QB:
        f = Fore.MAGENTA
        b = Back.RESET
        s = Style.NORMAL
    elif inColor == Color.POS_RB: # OK
        f = Fore.YELLOW
        b = Back.RED
        s = Style.NORMAL
    elif inColor == Color.POS_D:
        f = Fore.WHITE
        b = Back.RESET
        s = Style.NORMAL

    ps = f + b + s + f'{ps}' + e
    return ps

def d_clean_player_data(players):
  for player in players:
    player['posrank'] = int(player['posrank'])
    player['allrank'] = int(player['allrank'])
    player['name'] = player['name'].strip()
    player['team'] = player['team'].strip()

def d_print_player(p, pick, toFile=False):
  pos     = p["pos"]
  posrank = p["posrank"]
  allrank = p["allrank"]
  team    = p["team"]
  name    = p["name"]
  bye     = p["bye"]

  if p['onBoard'] and p['allrank'] >= pick:
      if   pos == 'WR':
           pos =     color_wrap(pos,     Color.POS_WR)
      elif pos == 'TE':
           pos =     color_wrap(pos,     Color.POS_TE)
      elif pos == 'K':
           pos =     color_wrap(pos,     Color.POS_K)
      elif pos == 'QB':
           pos =     color_wrap(pos,     Color.POS_QB)
      elif pos == 'RB':
           pos =     color_wrap(pos,     Color.POS_RB)
      elif pos == 'D':
           pos =     color_wrap(pos,     Color.POS_D)

  # bar graph for allrank
  NX = int(allrank*80/300)
  ARSTR = 'X'*NX + ' '*(80-NX) + '|'
  OB = 'OB _'
  if p['onBoard']:
      OB = 'OB 1'

  if toFile:
    if p['onBoard']:
        ps = '%2s %2d %3d |%25s| %3s bye=%2d' % \
            (pos, posrank, allrank, name, team, bye)
        ps = color_wrap(ps, Color.RESET)
        return ps

  # not to file
  else:
    ps = '%2s %2d %3d |%25s| %3s bye=%2d %s %s' % \
        (pos, posrank, allrank, name, team, bye, OB, ARSTR)

    if not p['onBoard']:
        #ps = color_wrap(ps, Color.RESET)    
        ps = color_wrap(ps, Color.OFF)
    elif p['allrank'] < pick:
        #ps = color_wrap(ps, Color.RESET)    
        ps = color_wrap(ps, Color.GOOD)

    return ps

def d_showboard(players):
  # show all players on board
  with open('output.dat', 'w') as f:
    RPLIST = reversed(sorted(players, key=lambda i: i['allrank']))
    for player in RPLIST:
      if player['onBoard']:
        ps = d_print_player(player, picknum(players) , toFile=True)
        f.write('{}\n'.format(ps))
  d_showpos('d' , players)
  d_showpos('k' , players)
  d_showpos('qb', players)
  d_showpos('rb', players)
  d_showpos('te', players)
  d_showpos('wr', players)
  d_plot_player(players)

def picknum(players):
  cnt = 0
  for player in players:
    if not player['onBoard']:
      cnt += 1
  return cnt

# show individual player position list
def d_showpos(pos, players):
  pos = pos.lower()
  with open('b_'+pos+'.dat', 'w') as f:
    RPLIST = reversed(sorted(players, key=lambda i: i['allrank']))
    for player in RPLIST:

      # Print player if still on board
      if player['onBoard'] and player['pos'].lower() == pos.lower():
        ps = d_print_player(player,picknum(players) ,  True)
        f.write('{}\n'.format(ps))

def sort_allrank(players):
    ps = sorted(players, key=itemgetter('allrank'), reverse=True)
    return ps

def find_players_by_key(testval, players, pkey):
    plist = []

    if testval == 'all_qb':
        return sort_allrank( [p for p in players if p['pos'] == 'QB' ])
    elif testval == 'all_rb':
        return sort_allrank( [p for p in players if p['pos'] == 'RB' ])
    elif testval == 'all_wr':
        return sort_allrank( [p for p in players if p['pos'] == 'WR' ])
    elif testval == 'all_te':
        return sort_allrank( [p for p in players if p['pos'] == 'TE' ])
    elif testval == 'all':
        return sort_allrank( players )

    isNum = get_int(testval) != -1

    if not isNum:
        testval = testval.lower()
    for player in sorted(players, key=itemgetter('allrank'), reverse=True):
        try:
            pval = player[pkey]
            if not isNum:
                pval = pval.lower()

                hasVal = pval.find(testval)
                if hasVal != -1:
                    plist.append(player)
            elif testval == pval:
                plist.append(player)
        except:
            pass
        
    return plist

def fv_helper(pkey):

    prompt = f'FIND [{pkey}] >>>'
    prompt = color_wrap(prompt, Color.PROMPT)
    findval = get_input(prompt)

    if pkey == 'allrank':
        findval = get_int(findval)

    return findval

def change_player_status(action_str, player):
        action_str = action_str.lower()
        #print('board [r]emove [t]oggle [a]dd')
        r_s = [ 'r', 'remove']
        t_s = [ 't', 'toggle']
        a_s = [ 'a', 'add']

        if action_str in r_s:
            player['onBoard'] = False
        elif action_str in t_s:
            player['onBoard'] = not player['onBoard']
        elif action_str in a_s:
            player['onBoard'] = True


def d_find_player(players):
  prompt_str = 'find by [napt] name, allrank, pos, team'
  prompt_str = color_wrap(prompt_str, Color.PROMPT)
  print(prompt_str)

  ps = color_wrap(': ', Color.PROMPT)
  choice = get_input(ps).lower()

  doneFlags =[
      'done',
      '-1',
      -1,
  ]

  if choice == 't' or choice == 'team':
      pkey = 'team'
      allteams = [ p['team'] for p in players ]
      allteams = [ t for t in allteams if t.find('1:') == -1 ]
      allteams = set(allteams)
      tstr = ' '.join(allteams)
      tstr = color_wrap(tstr, Color.CHILL)
      print(tstr)

  elif choice == 'a' or choice == 'allrank':
      pkey = 'allrank'
  elif choice == 'p' or choice == 'pos':
      pkey = 'pos'
      positions = set([ p['pos'] for p in players ])
      pstr = ' '.join(positions)
      print( color_wrap(pstr, Color.CHILL) )
  else:
      pkey = 'name'
      names = list(set([ p['name'].split()[-1] for p in players if p['allrank'] < 140]))
      names.sort()
      pstr = ' '.join(names)
      print( color_wrap(pstr, Color.CHILL) )
  
  print(color_wrap( f'finding by: {pkey}', Color.CHILL))
  findval = fv_helper(pkey)

  while findval not in doneFlags:

    matched_players = find_players_by_key(findval, players, pkey)

    team_picks = get_pick_numbers(7)

    showFlag = True
    pick = picknum(players)
    for player in matched_players:
        ps = d_print_player(player, pick)
        if player['allrank']+1 in team_picks:
            delimstr = f'{int(player["allrank"] / 12) + 1} {player["allrank"]+1} ' + '-'*(80+42)
            delimstr = color_wrap(delimstr, Color.CHILL)
            print(delimstr)
        if player['allrank'] < pick and showFlag:
            showFlag = False
            delimstr = f'PICK # {pick} ' + '-'*(80+42)
            delimstr = color_wrap(delimstr, Color.DELIM)
            print(delimstr)
        print(ps)
    if len(matched_players) == 1:
        istr = '[ACTION]: rm toggle add, rta >>>'
        istr = color_wrap(istr, Color.CHILL)
        rta = input(istr)
        change_player_status(rta, matched_players[0])

    d_showboard(players)
    findval = fv_helper(pkey)


# remove player matching choice in allrank
def d_rm_player(players):
  print('remove by allrank #')
  allrank = get_int(get_input("Who to remove?: "))
  while allrank > 0:

    for player in players:
      if player['allrank'] == allrank:
        player['onBoard'] = False

        strpick = 'PICK [%3d], removing player: %s' % (picknum(players), player)
        print(strpick)
    d_showboard(players)
    allrank = get_int(get_input("Who to remove?: "))

def d_correct_player(players):
  print('put player back on board by allrank #')
  allrank = get_int(get_input("Who to correct?: "))
  while allrank > 0:

    for player in players:
      if player['allrank'] == allrank:
        player['onBoard'] = True
        print("correcting player",player)
    d_showboard(players)
    allrank = get_int(get_input("Who to correct?: "))

def d_indirect(c, players):
  switcher={
      'f':d_find_player,
      'r':d_rm_player,
      'c':d_correct_player,
      'p':d_plot_player,
      }
  func=switcher.get(c,lambda players :'Invalid')
  return func(players)


def d_plot_player(players):
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
    RPLIST = sorted(players, key=itemgetter('allrank'), reverse=True)
    for p in RPLIST:
      posrank = p['posrank']
      allrank = p['allrank']
      pos     = p['pos']
      onBoard = p['onBoard']
      if onBoard:
        if pos.lower() == 'wr':
          #wr_n.append(pos+'-'+name)
          wr_a.append(allrank)
          wr_p.append(posrank)
        elif pos.lower() == 'qb':
          #qb_n.append(pos+'-'+name)
          qb_a.append(allrank)
          qb_p.append(posrank)
        elif pos.lower() == 'rb':
          #rb_n.append(pos+'-'+name)
          rb_a.append(allrank)
          rb_p.append(posrank)
        elif pos.lower() == 'te':
          #te_n.append(pos+'-'+name)
          te_a.append(allrank)
          te_p.append(posrank)
        elif pos.lower() == 'd':
          #d_n.append(pos+'-'+name)
          d_a.append(allrank)
          d_p.append(posrank)
        elif pos.lower() == 'k':
          #k_n.append(pos+'-'+name)
          k_a.append(allrank)
          k_p.append(posrank)
      else:
        #t_n.append(pos+'-'+name)
        t_a.append(allrank)
        t_p.append(posrank)


    pick = picknum(players)
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
