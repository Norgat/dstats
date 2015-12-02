# -*- encoding: utf-8 -*-


# DOC: https://openpyxl.readthedocs.org/en/default/
import openpyxl as excel
from data.excel import *
from analyze.common import *

data_path = "d:\dota\data\Dota 2.xlsx"
wb = excel.load_workbook(data_path)

tournaments = []

print "Sheet list:"
for sheet_name in wb.get_sheet_names():
  print "%s: %s" % (sheet_name, get_sheet_type(wb[sheet_name]))
  if (get_sheet_type(wb[sheet_name])) == "tournament":
    tournaments.append( TournamentExcel(wb[sheet_name]) )

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