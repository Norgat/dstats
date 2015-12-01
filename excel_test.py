# -*- encoding: utf-8 -*-

# DOC: https://openpyxl.readthedocs.org/en/default/
import openpyxl as excel
import openpyxl.styles as excel_styles

data_path = "d:\dota\data\Dota 2.xlsx"
wb = excel.load_workbook(data_path)

RC, LC = "B2", "F17"

def get_sheet_type(sheet):
  if sheet["A1"].value == "type":
    return sheet["B1"].value
  else:
    return None

ColorToCodes = {
  'FFFFFFFF': 0, # не играл на предыдущем турнире
  'FF00B0F0': 1, # играли вместе на предыдущем турнире в команде 1
  'FF0070C0': 2, # играли вместе на предыдущем турнире в команде 2
  'FF92D050': 3  # играл на предыдущем турнире
}

# кешируем обратную мэпу для код фона -> цвет
CodesToColor = {}
for color in ColorToCodes.keys():
  CodesToColor[ ColorToCodes[color] ] = color


class Player:
  """Dota 2 Player"""
  def __init__(self, nickname, team, sheet, row_num, col_num):
    self.Nickname = nickname.lower()
    self.Team = team
    self.Sheet = sheet
    self.Row = row_num
    self.Column = col_num
    self.Cell = sheet.cell(row = self.Row, column = self.Column)

    fgColor = self.Cell.fill.fgColor.rgb
    if type(fgColor) is str:
      self.PrevCode = ColorToCodes.get(fgColor, 0)
    else:
      self.PrevCode = 0

  def __eq__(self, other):
    return self.Nickname == other.Nickname

  def __hash__(self):
    return hash(self.Nickname)

  def __repr__(self):
    return "< %s | %s >" % (self.Nickname, self.Team.Tag)

  def write(self, **kwargs):
    sheet = self.Sheet
    if "sheet" in kwargs:
      sheet = kwargs["sheet"]
    sheet.cell(row = self.Row, column = self.Column).value = self.Nickname

    # стиль ячейки не может быть изменён, только перезаписан
    fill_pattern = excel_styles.PatternFill(patternType = 'solid', fgColor = excel_styles.Color(CodesToColor[self.PrevCode]))
    sheet.cell(row = self.Row, column = self.Column).fill = fill_pattern


class Team:
  """Dota 2 team class."""
  def __init__(self, sheet, row_num):
    self.Tag = str(sheet.cell(row = row_num, column = 1).value)
    self.Sheet = sheet
    self.Row = row_num

    self.Players = set([])
    for i in xrange(2, 7):
      self.Players.add(Player(str(sheet.cell(row = row_num, column = i).value), self, sheet, row_num, i))

    self.Top = int( sheet.cell(row = row_num, column = 7).value )

  def __repr__(self):
    return self.Tag

  def write(self, **kwargs):
    sheet = self.Sheet

    if "sheet" in kwargs:
      sheet = kwargs["sheet"]

    sheet.cell(row = self.Row, column = 1).value = self.Tag
    sheet.cell(row = self.Row, column = 7).value = self.Top


    for player in self.Players:
      player.write(**kwargs)

    if "topdiff" in kwargs:
      if kwargs["topdiff"]:
        sheet.cell(row = self.Row, column = 9).value = self.TopDiff


class Tournament:
  """Dota 2 tournament class."""
  def __init__(self, sheet):
    self.Title = str(sheet["B2"].value)
    self.NumberOfTeams = int(sheet["D1"].value)
    self.EndDate = sheet["D2"].value
    self.Sheet = sheet

    self.Teams = {}
    self.Players = {}

    for i in xrange(4, 4 + self.NumberOfTeams):
      tmp_team = Team(sheet, i)
      self.Teams[tmp_team.Tag] = tmp_team
      
      for player in tmp_team.Players:
        self.Players[player.Nickname] = player

  def __repr__(self):
    return "Tournament: %s" % self.Title

  def write(self, **kwargs):
    sheet = self.Sheet
    if "sheet" in kwargs:
      sheet = kwargs["sheet"]

    # write type
    sheet["A1"] = "type"
    sheet["B1"] = "tournament"

    # write title
    sheet["A2"] = "title"
    sheet["B2"] = self.Title

    # write Number of teams
    sheet["C1"] = "Number of teams"
    sheet["D1"] = self.NumberOfTeams

    # write data column titles
    sheet["A3"], sheet["B3"], sheet["C3"] = "Team", "Player 1", "Player 2"
    sheet["D3"], sheet["E3"], sheet["F3"] = "Player 3", "Player 4", "Player 5"
    sheet["G3"] = "Top"

    if "topdiff" in kwargs:
      if kwargs["topdiff"]:
        sheet["I3"] = "Top change"

    for tag in self.Teams.keys():
      self.Teams[tag].write(**kwargs)


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