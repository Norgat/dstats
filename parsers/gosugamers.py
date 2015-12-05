# -*- encoding: utf-8 -*-

from data.model import *
import urllib
from bs4 import BeautifulSoup

tournaments_list_test_url = "http://www.gosugamers.net/dota2/events/list?type=past&page="


def get_tournament_list(page_url, from_page, to_page):
  result = []
  for i in xrange(from_page, to_page+1):
    f = urllib.urlopen(tournaments_list_test_url + str(i))
    data = f.read()
    soup = BeautifulSoup(data)

    for record in soup.find_all("div", "event columns"):
      result.append("http://www.gosugamers.net" + str(record.div.a["href"]))

  return result


# print get_tournament_list(tournaments_list_test_url, 1, 1)

def some_code():
  esl_one_link = "http://www.gosugamers.net/dota2/events/299-esl-one-2015-frankfurt"

  data = urllib.urlopen(esl_one_link)
  soup = BeautifulSoup(data)


  def get_main_bracket(brackets):
    for bracket in brackets:
      bracket_type = bracket.h2.span.string
      if "Main Event" in bracket_type:
        return  bracket
    return None


  main_event = get_main_bracket(soup.find_all("div", "box box-tournament-\-knockout-tournament"))
  rounds = main_event.find_all("div", "round")


  def intTryParse(value):
    try:
      return int(value)
    except ValueError:
      return None


  for R in rounds:
    print intTryParse(R.h3.string[6:])
    matches = R.find_all("div", "match")
    for M in matches:
      #print M
      teams = [t.span["title"] for t in M.find_all("div", "opponent")]
      print teams


match_link = "http://www.gosugamers.net/dota2/tournaments/6642-esl-one-2015-frankfurt/1771-main-event/6644-the-main-event/matches/81029-virtus-pro-dota2-vs-alliance"

def parse_match(link):
  data = urllib.urlopen(link)
  soup = BeautifulSoup(data)

  teams_roster = soup.find("div", "lineup-conent dota2")

  team_one = teams_roster.find("div", "row-0 full")
  team_two = teams_roster.find("div", "row-1 full")

  result = {}

  for team in [team_one, team_two]:
    tag = " ".join(team.find("label", "team-name").string.split())
    player_sources = team.find_all("div", "pick-row")
    result[tag] = [p.a.string for p in player_sources]

  return result

print parse_match(match_link)



