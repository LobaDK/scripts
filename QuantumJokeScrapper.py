from bs4 import BeautifulSoup
import requests
import random

url = 'https://upjoke.com/quantum-jokes'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
for link in soup.find_all('div', {'class': 'joke-content'}):
    