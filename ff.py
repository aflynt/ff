#!/usr/bin/python3
import matplotlib.pyplot as plt
from FF import *

pos_files = [
  'jpos_d.json',
  'jpos_k.json',
  'jpos_qb.json',
  'jpos_rb.json',
  'jpos_te.json',
  'jpos_wr.json',
]

players = []
for f in pos_files:
  #data += read_file(f)
  players += get_list_of_players(f)

sorted(players, key=lambda i : i['allrank'])

# Sort the data based on allrank
#data.sort(key = sort_allrank)

#    p = data[player]
#    posrank = p[0]
#    allrank = p[1]
#    name    = p[2]
#    team    = p[3]
#    price   = p[4]
#    bye     = p[5]
#    pos     = p[6]
#    onBoard = p[7]

d_clean_player_data(players)

# [ ] find_player
# [ ] rm_player
# [ ] correct_player
# [ ] plot_player
# [x] showboard
# [x] showpos
# [x] print_player
# [ ] picknum

if __name__ == "__main__":
  while True:
    ps = '''
        Pick action:
          f == find player(s)
          r == remove player(s)
          c == correct player(s) status
          p == plot player(s)
          '''
    ps = color_wrap(ps, Color.PROMPT)
    print(ps)

    prompt_str = color_wrap("Choice: ", Color.PROMPT)
    pick = get_input(prompt_str)

    d_indirect(pick,players)

    d_showboard(players)
