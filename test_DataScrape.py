# Web scrapes data from basketball-reference, as it is the most up to date source for NBA data.
# First testing if data can be retrieved from the site and outputted to the screen

# Importing the necessary libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.request


page = urllib.request.urlopen('https://www.basketball-reference.com/boxscores/202202060CLE.html')
soup = BeautifulSoup(page, features='html.parser')
# print(soup.prettify())

print(soup.find_all())

