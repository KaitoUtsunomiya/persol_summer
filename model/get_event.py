import datetime
import requests
from bs4 import BeautifulSoup
import re
import time
from tqdm import tqdm
import pandas as pd
from geopy.distance import geodesic

def get_event(original_location,day):
    # 住所の中から郵便番号を抽出する
    location = re.findall('\d{3}-\d{4}', original_location)
    #郵便番号から県情報を取得
    k = zipinfo(location[0])
    # 日付情報の取得
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%Y/%m/%d')
    d = dt_now.replace('/', '')
    d  =day.replace('-','')
    # url
    event_url = 'https://www.livebu.com/search?p=1&co=event&c=1001&k=' + k +'&d=' + str(d)
    #rint(event_url)
    headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
    r = requests.get(event_url, headers=headers_dic)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup)
    elems = soup.find(class_="column_right").find_all(href=re.compile("/hall/"))
    hall_id = []
    for i in range(len(elems)):
        m = re.findall(r'/hall/(.*)"', str(elems[i]))
        hall_id.append(m[0])
    event = []
    for each in elems[0:]:
        event.append(each.get_text().strip('\n'))
    #rint(event)
    #rint(hall_id)
    list3 = [[] for i in range(len(event))]
    for i in range(len(event)):
        list3[i].append(event[i])
        list3[i].append(hall_id[i])
    return list3, event_url

def zipinfo(zipcode):
    url = "https://zip-cloud.appspot.com/api/search?zipcode=" + str(zipcode)
    x = requests.get(url)
    x = x.json()
    x = x['results']
    y = pd.DataFrame(x)
    return y['address1'][0]

def get_hall_location(hall_l):
    location = []
    capacity = []
    headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
    for i in range(len(hall_l)):
        
        hall_url = 'https://www.livebu.com/hall/' + str(hall_l[i][1])
        r = requests.get(hall_url, headers=headers_dic)
        soup = BeautifulSoup(r.text, 'html.parser')
        #print(soup)
        elems = soup.find(class_="hall_address_box").find('div')
        #print(elems)
        cap = soup.find(class_="dtl_cap_main_num")
        location.append(elems.get_text())
        capacity.append(cap.get_text())
    return location, capacity

def get_lat_lon_from_address(address_l):
    """
    address_lにlistの形で住所を入れてあげると、latlonsという入れ子上のリストで緯度経度のリストを返す関数。
    >>>>get_lat_lon_from_address(['東京都文京区本郷7-3-1','東京都文京区湯島３丁目３０−１'])
    [['35.712056', '139.762775'], ['35.707771', '139.768205']]
    """
    url = 'http://www.geocoding.jp/api/'
    latlons = []
    for address in tqdm(address_l):
        payload = {"v": 1.1, 'q': address}
        r = requests.get(url, params=payload)
        ret = BeautifulSoup(r.content,'lxml')
        if ret.find('error'):
            raise ValueError(f"Invalid address submitted. {address}")
        else:
            lat = ret.find('lat').string
            lon = ret.find('lng').string
            latlons.append([lat,lon])
            time.sleep(1)
    return latlons

def get_near_event(event_hall_info,location):
    
    # (緯度, 経度)
    event_hall = []
    location = get_lat_lon_from_address(location)
    location = (float(location[0][0]),float(location[0][1]))
    for i in range(len(event_hall_info)):
        event = (float(event_hall_info[i][4]),float(event_hall_info[i][5]))
        dis = geodesic(location,event).km
        if(dis <= 2):
            event_hall.append(event_hall_info[i])
    return event_hall

def main(location,day):
    location = location[0].split(',')
    print(location)
    event_hall, event_url = get_event(location[0],day)
    event_hall_location, event_hall_capacity = get_hall_location(event_hall)
    for i in range(len(event_hall)):
        event_hall[i].append(event_hall_location[i])
        event_hall[i].append(event_hall_capacity[i])
    print(event_hall)
    hall_place = get_lat_lon_from_address(event_hall_location)
    event_hall_place = list(map(list.__add__, event_hall, hall_place))
    #print(event_hall_place)
    event_info = get_near_event(event_hall_place, [location[1]])
    event = day + 'のイベント情報\n'
    if (len(event_info)!=0):
        for i in range(len(event_info)):
            event_str = '会場 :' + event_info[i][0] +', 住所 :' + event_info[i][2] + ', 収容人数 :' + event_info[i][3]
            event = event + event_str + '\n'
    elif(len(event_info) == 0 ):
        event = event + '近くの会場で行われるイベントはありません。'
    event = event + '\n詳細:' + event_url
    #return get_near_event(event_hall_place, [location[1]]), event_url
    f = open("controller/static/text/event.txt", "w", encoding='utf-8')
    f.write(event)
    f.close()