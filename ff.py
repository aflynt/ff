#!/usr/bin/python3
import matplotlib.pyplot as plt
from FF import *

pos_files = [
  'pos_d.txt',
  'pos_k.txt',
  'pos_qb.txt',
  'pos_rb.txt',
  'pos_te.txt',
  'pos_wr.txt',
]

data = []
for f in pos_files:
  data += read_file(f)

# Sort the data based on allrank
data.sort(key = sort_allrank)

#    p = data[player]
#    posrank = p[0]
#    allrank = p[1]
#    name    = p[2]
#    team    = p[3]
#    price   = p[4]
#    bye     = p[5]
#    pos     = p[6]
#    onBoard = p[7]

clean_player_data(data)


if __name__ == "__main__":
  while True:
    print(''' Pick action:
          f == find player(s)
          r == remove player(s)
          c == correct player(s) status
          p == plot player(s)
          ''')
    pick = get_input("Choice: ")
    indirect(pick,data)
    showboard(data)
