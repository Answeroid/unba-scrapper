from bs4 import BeautifulSoup
import requests

url = 'https://erau.unba.org.ua/profile/1'
response = requests.get(url)
# TODO deconstruct URL to base and specific parts
# TODO check response code is 200
# TODO check that page exists
# TODO create logger and write everything to logs/log file
content = response.text
#content_json = response.json()

soup = BeautifulSoup(content, 'html.parser')
print(soup.prettify())
# TODO save json and csv files to results
# TODO convert json and csv to simple html to easily search through the list
