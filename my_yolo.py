import requests
from bs4 import BeautifulSoup


source = requests.get('http://www.weather.go.kr/weather/observation/currentweather.jsp')
soup = BeautifulSoup(source.content, "html.parser")

table = soup.find('table', {'class': 'table_develop3'})
data = []

for tr in table.find_all('tr'):
    tds = list(tr.find_all('td'))
    for td in tds:
        if td.find('a'):
            point = td.find('a').text
            weather = tds[1].text
            print("{0:<7} {1:<7}".format(point, weather))
            data.append([point, weather])
print(data)