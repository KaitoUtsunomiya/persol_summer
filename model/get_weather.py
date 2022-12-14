import datetime
import requests
from bs4 import BeautifulSoup
import re

# 位置情報からその日の天気を返す
def get_weather(original_location,len,day):
    original_location = ''.join(original_location)
    # 住所の中から郵便番号を抽出する
    location = re.findall('\d{3}-\d{4}', original_location)
    # 1回目のスクレイピングでは住所を検索し、候補から取ってくる
    url = "https://weather.yahoo.co.jp/weather/search/?p=" + location[0]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find(class_="serch-table")
    # 2回目のスクレイピングで用いるURLを得る
    location_url = content.find('a').get('href')
    print(location_url)
    dt_now = datetime.datetime.now()
    today = str(dt_now).split()[0]
    if (len != '今日'):
        result1 = get_tommorow_weather(location_url)
        result1 = ('{}の明日の天気は\n'.format(original_location) + '\n'.join(result1) + 'です。\n')
        result2 = get_weekly_weather(location_url)
        result2 = ('{}の1週間の天気は\n'.format(original_location) + '\n'.join(result2) + 'です。\n')
        result = result1 + result2
    elif(len == '今日'):
        result = get_today_weather(location_url)
        result = ('{}の今日の天気は\n'.format(original_location) + '\n'.join(result) + 'です。\n')
        dt_now = datetime.datetime.now()
        result = result + '現在時刻は{}です。'.format(dt_now)
    result.replace('\n', '<br>')  
    f = open("controller/static/text/weather.txt", "w", encoding='utf-8')
    f.write(result)
    f.close()

def get_today_weather(location_url):
    r = requests.get(location_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    content = soup.find(id='yjw_pinpoint_today').find_all('td')
    # print(content)
    warn = soup.find(id='wrnrpt').find_all('dd')
    # print(warn)
    info = []
    warn_info = []
    
    for each in content[1:]:
        info.append(each.get_text().strip('\n'))
    if(len(warn) != 0):
        for each in warn[0]:
            warn_info.append(each.get_text().strip('\n'))
    elif(len(warn) == 0):
        warn_info.append('None')
    warn_info  = '\n'.join(warn_info)
    # print(warn_info)
    # 時間
    time = info[:8]
    # 天気
    weather = info[9:17]
    # 気温
    temperature = info[18:26]
    # 湿度
    humidity = info[27:35]
    # 降水量
    precipitation = info[36:44]
    # 上の3つの情報を合わせる
    weather_info = [(time[i], weather[i], temperature[i],humidity[i],precipitation[i], warn_info) for i in range(8)]
    # print(weather_info)

    # result = [('{0[0]}: {0[1]}, {0[2]}°C'.format(weather_info[i])) for i in range(8)]
    result = [('{0[0]}: {0[1]}, {0[2]}°C, {0[3]}%, {0[4]}ml, {0[5]}'.format(weather_info[i])) for i in range(8)]
    return result

def get_tommorow_weather(location_url):
    r = requests.get(location_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    content = soup.find(id='yjw_pinpoint_tomorrow').find_all('td')
    # print(content)
    info = []
    warn_info = []
    
    for each in content[1:]:
        info.append(each.get_text().strip('\n'))
    warn_info.append('None')
    warn_info  = '\n'.join(warn_info)
    # print(warn_info)
    # 時間
    time = info[:8]
    # 天気
    weather = info[9:17]
    # 気温
    temperature = info[18:26]
    # 湿度
    humidity = info[27:35]
    # 降水量
    precipitation = info[36:44]
    # 上の3つの情報を合わせる
    weather_info = [(time[i], weather[i], temperature[i],humidity[i],precipitation[i], warn_info) for i in range(8)]
    # print(weather_info)

    # result = [('{0[0]}: {0[1]}, {0[2]}°C'.format(weather_info[i])) for i in range(8)]
    result = [('{0[0]}: {0[1]}, {0[2]}°C, {0[3]}%, {0[4]}ml, {0[5]}'.format(weather_info[i])) for i in range(8)]
    return result

def get_weekly_weather(location_url):
    r = requests.get(location_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    content = soup.find(id='yjw_week').find_all('small')
    info = []
    for each in content[0:]:
        info.append(each.get_text().strip('\n'))
    weather_info = []
    for i in range(6):
        weather = info[i+1].replace('\n','').replace(' ','') + ': ' + info[i+8].strip() + ', ' + info[i+15].replace('\n','°C, ') + '°C, ' +info[i+22].strip() + '%'
        weather_info.append(weather)
    return weather_info

def main(original_location,len, day):
    print(get_weather)
    get_weather(original_location,len,day)