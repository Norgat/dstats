# -*- encoding: utf-8 -*-

def colorize_tournament(current_tournament, previous_tournament):
  for tag in current_tournament.Teams.keys():
    team = current_tournament.Teams[tag]

    prev_teams = {}
    for player in team.Players:
      if player.Nickname in previous_tournament.Players:
        tmp_player = previous_tournament.Players[player.Nickname]
        prev_tag = tmp_player.Team.Tag

        if prev_tag in prev_teams:
          prev_teams[prev_tag].append(player)
        else:
          prev_teams[prev_tag] = [player]

    prev_teams_count = 1
    for tag in prev_teams.keys():
      if len(prev_teams[tag]) == 1:
        prev_teams[tag][0].PrevCode = 3
      else:
        for player in prev_teams[tag]:
          player.PrevCode = prev_teams_count
        prev_teams_count += 1


def compute_teams_top_diff(current_tournament, previous_tournament):
  for tag in current_tournament.Teams.keys():
    current_top = current_tournament.Teams[tag].Top

    max_prev_top = 0
    for player in current_tournament.Teams[tag].Players:
      if player.Nickname in previous_tournament.Players and (player.PrevCode in set([1,2])):
        prev_player_place = previous_tournament.Players[player.Nickname].Team.Top
        if max_prev_top == 0:
          max_prev_top = prev_player_place
        elif max_prev_top > prev_player_place:
          max_prev_top = prev_player_place

    if max_prev_top == 0:
      current_tournament.Teams[tag].TopDiff = 0
    else:
      current_tournament.Teams[tag].TopDiff = max_prev_top - current_top