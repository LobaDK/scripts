from bs4 import BeautifulSoup
import requests

titles = []
i = 0
url = 'https://upjoke.com/quantum-jokes'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
for title in soup.find_all('h3', {'class': 'joke-title'}):
    titles.append(title.get_text())
with open('./quantumjokes.txt', 'w') as jokes:
    for punchline in soup.find_all('div', {'class': 'joke-body'}):
        if '<br>' in punchline:
            punchline.replace('<br>', ' ')
        if "b'" in punchline.get_text():
            punchline.get_text().encode().replace("b'", '')
        try:
            jokes.write(f'{titles[i]} {punchline.get_text()}\n\n')
        except:
            pass
        i += 1
jokes.close()