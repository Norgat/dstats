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