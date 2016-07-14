import requests
from pyquery import PyQuery as pq


def get_tomorrow_weather():
    response = requests.get('http://www.weather.com.cn/weather/101020100.shtml')
    response.encoding = 'utf8'
    html = pq(response.text)
    html = html('div#7d ul li.sky')
    for li in html:
        date = html(li)('h1').text()
        if date.find('明天') > -1:
            weather = html(li)('p').eq(0).text()
            temperature = html(li)('p').eq(1).text()
            wind = html(li)('p.win i').text()
            print(weather, temperature, wind)
            return ({'weather': weather, 'temperature': temperature, 'wind': wind})
