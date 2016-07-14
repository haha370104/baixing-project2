import requests
from pyquery import PyQuery as pq


def get_tomorrow_weather():
    response = requests.get('http://www.weather.com.cn/weather/101020100.shtml')
    response.encoding = 'utf8'
    html = pq(response.text)
    html = html('div#7d ul li.sky')
    result = []
    for li in html:
        date = html(li)('h1').text()
        # if date.find('明天') > -1:
        weather = html(li)('p').eq(0).text()
        temperature = html(li)('p').eq(1).text()
        result.append({'date': date, 'weather': weather, 'temperature': temperature})
    return result


if __name__ == '__main__':
    print(get_tomorrow_weather())
