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


esl_one_link = "http://www.gosugamers.net/dota2/events/299-esl-one-2015-frankfurt"

data = urllib.urlopen(esl_one_link)
soup = BeautifulSoup(data)


def get_main_bracket(brackets):
  for bracket in brackets:
    bracket_type = bracket.h2.span.string
    if bracket_type == "Main Event":
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


