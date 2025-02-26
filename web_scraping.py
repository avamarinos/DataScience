import pandas as pd
import requests
from bs4 import BeautifulSoup #parsing HTML

def ScrapeTable(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text,"html.parser")
  table = soup.find("table", {"class":"wikitable"})
  header_text = [header.text.strip() for header in table.find_all("th")] # for loop in one line
  return header_text
  #return table
  #return soup
  # get rid of 1s and 13s

print(ScrapeTable("https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"))