

def get_order_top_down(picks, teams):

    p_t = [ (p,t) for p,t in zip(picks, teams)]
    return p_t

def get_order_bottom_up(picks, teams):

    teams = reversed(teams)

    p_t = [ (p,t) for p,t in zip(picks, teams)]
    return p_t

def get_round_pics(round, teams):

    past_picks = (round-1)*len(teams)
    pick_start = past_picks+1
    pick_end   = past_picks+len(teams)

    picks = [ i for i in range(pick_start, pick_end+1)]

    return picks

def print_round(round, teams):

    picks = get_round_pics(round, teams)

    if round % 2 == 1:
        p_t = get_order_top_down(picks, teams)

        for p,t in p_t:
            print(f'pick: {p:2d}, team: {t:2d}')
    else:
        p_t = get_order_bottom_up(picks, teams)
        for p,t in p_t:
            print(f'pick: {p:2d}, team: {t:2d}')

def helper_get_picks_for_team(round, teams, team_num):

    picks = get_round_pics(round, teams)

    if round % 2 == 1:
        p_t = get_order_top_down(picks, teams)
        team_pick = [ p for p,t in p_t if t == team_num]
    else:
        p_t = get_order_bottom_up(picks, teams)
        team_pick = [ p for p,t in p_t if t == team_num]

    return team_pick[0]

def get_team_picks(teams, team_num, rounds):

    team_picks = []
    for r in rounds:
        rpicks = helper_get_picks_for_team(r, teams, team_num)
        team_picks.append(rpicks)

    return team_picks


def get_pick_numbers(draft_order):
    N_teams = 12
    team_num =  draft_order
    Nrounds = 15
  
    teams = [ i for i in range(1, N_teams+1)]
    rounds = range(1, Nrounds+1)
  
    team_picks = []
  
    team_picks = get_team_picks(teams, team_num, rounds)
  
    #for r,p in zip(rounds,team_picks):
    #    print(f' round : {r}, picks = {p}')

    return team_picks

