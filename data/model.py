# -*- encoding: utf-8 -*-


class Player(object):
  def __init__(self, nickname, team):
    self.Nickname = nickname
    self.Team = team

  def __eq__(self, other):
    return self.Nickname == other.Nickname

  def __hash__(self):
    return hash(self.Nickname)


class Team(object):
  def __init__(self, tag):
    self.Tag = tag


class Tournament(object):
  def __init__(self, title, teams, end_date):
    self.Title = title
    self.Teams = teams
    self.EndDate = end_date

    self.Players = {}
    for tag in self.Teams.keys():
      tmp_team = self.Teams[tag]

      for player in tmp_team.Players:
        self.Players[player.Nickname] = player