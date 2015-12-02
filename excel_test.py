# -*- encoding: utf-8 -*-

# DOC: https://openpyxl.readthedocs.org/en/default/
import openpyxl as excel
from data.excel import *

data_path = "d:\dota\data\Dota 2.xlsx"
wb = excel.load_workbook(data_path)


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


tournaments = []

print "Sheet list:"
for sheet_name in wb.get_sheet_names():
  print "%s: %s" % (sheet_name, get_sheet_type(wb[sheet_name]))
  if (get_sheet_type(wb[sheet_name])) == "tournament":
    tournaments.append( Tournament(wb[sheet_name]) )

# test adding new sheet
new_sheet_name = "New sheet " + str( len(tournaments) )
new_sheet = wb.create_sheet()
new_sheet.title = new_sheet_name

TI_2012 = tournaments[1]
TI_2013 = tournaments[2]
colorize_tournament(TI_2013, TI_2012)
compute_teams_top_diff(TI_2013, TI_2012)
TI_2013.write(sheet = new_sheet, topdiff = True)

# Необходимо закрыть Excel для того, чтобы сохранить workbook на диск.
# Если сохранение не требуется, то закрывать Excel не нужно.
wb.save(data_path)


# print "\n\nTeams list:"
# for T in tournaments:
#   print ""
#   print T.Title  
#   print "Number of teams: %d" % len(T.Teams.keys())
#   print str(T.Teams)

# tmp = set(tournaments[1].Players).intersection(set(tournaments[0].Players))

# print "\nPlayers: "
# print tournaments[1].Players
# print "Count: %d" % len(tournaments[1].Players)

# print "\nIntersection: "
# print tmp
# print "Count: %d" % len(tmp)