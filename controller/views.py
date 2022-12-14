from webbrowser import get
import csv
import math
import re
import pandas as pd
from flask import render_template,request, url_for
from controller import app
import datetime
import model.get_event as ge
import model.get_weather as gw
import model.graph as graph
import model.create_csv as cre_csv
import model.location_csv as loc_csv

#トップページ
#予測の入力画面へ
@app.route('/')
def login():
    return render_template('login.html')



@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        if request.args.get('way') == 'after':
            day_0 = request.args.get('day')
            day = datetime.datetime.strptime(day_0, '%Y-%m-%d')
            tomorrow_0 = (day + datetime.timedelta(1)).date()
            tomorrow = tomorrow_0.strftime('%Y-%m-%d')

            length = request.args.get('len')
            if length == '1日':
                res = 'の来客人数予測です。'
            elif length == '1週間':
                res = 'から1週間の来客人数予測です。'
            else:
                res = 'から1か月間の来客人数予測です。'

            per_person = request.args.get('per_person')

            graph.main(length, tomorrow)

            csv_day = tomorrow.split('-')
            csv_day = csv_day[1] + '_' + csv_day[2]
            csv_info = 'CSV_files/' + csv_day + '_1day.csv'
            df = pd.read_csv(csv_info, encoding = 'shift-jis')
            per_list = df['人数'].to_list()
            per_list = per_list[0:10]
            num = re.sub( r'\D', '', per_person)
            for i in range(len(per_list)):
                per_list[i] = math.ceil(per_list[i]/int(num))

            return render_template('predict.html', ans=res, day=tomorrow, len=length, today=tomorrow, per_person=per_person, per_list=per_list)
        
        elif request.args.get('way') == 'before':
            day_0 = request.args.get('day')
            day = datetime.datetime.strptime(day_0, '%Y-%m-%d')
            yesterday_0 = (day - datetime.timedelta(1)).date()
            yesterday = yesterday_0.strftime('%Y-%m-%d')

            length = request.args.get('len')
            if length == '1日':
                res = 'の来客人数予測です。'
            elif length == '1週間':
                res = 'から1週間の来客人数予測です。'
            else:
                res = 'から1か月間の来客人数予測です。'

            per_person = request.args.get('per_person')

            graph.main(length, yesterday)

            csv_day = yesterday.split('-')
            csv_day = csv_day[1] + '_' + csv_day[2]
            csv_info = 'CSV_files/' + csv_day + '_1day.csv'
            df = pd.read_csv(csv_info, encoding = 'shift-jis')
            per_list = df['人数'].to_list()
            per_list = per_list[0:10]
            num = re.sub( r'\D', '', per_person)
            for i in range(len(per_list)):
                per_list[i] = math.ceil(per_list[i]/int(num))

            return render_template('predict.html', ans=res, day=yesterday, len=length, today=yesterday, per_person=per_person, per_list=per_list)

        elif request.args.get('way') == 'normal':
            day = request.args.get('day')
            today = request.args.get('today')
            res = request.args.get('res')
            length = request.args.get('len')
            per_person = request.args.get('per_person')
            per_list = request.args.get('per_list')
            per_list = eval(per_list)
            return render_template('predict.html', ans=res, day=day, len=length, today=today, per_person=per_person, per_list=per_list)
    
    else:
        length = request.form.get('len')
        day = request.form.get('day')
        per_person = request.form.get('per_person')
        csv_day = day.split('-')
        csv_day = csv_day[1] + '_' + csv_day[2]
        #住所の取得
        with open('CSV_files/location.csv',encoding="utf-8") as f:
            line = f.read()
            location_list = [line.strip()]
        #天気の予測
        #gw.main(location_list,length,day)
        #イベントの取得
        #ge.main(location_list,day)
        #予測に使用するCSVの作成
        cre_csv.main(length, day)
        #予測
        #グラフの作成
        # '1' が返ってきたら下を実行
        graph.main(length, day)
        if length == '1日':
            res = 'の来客人数予測です。'
        elif length == '1週間':
            res = 'から1週間の来客人数予測です。'
        else:
            res = 'から1か月間の来客人数予測です。'
        nowadays = datetime.datetime.now()
        tomorrow = nowadays + datetime.timedelta(1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')

        csv_info = 'CSV_files/' + csv_day + '_1day.csv'
        df = pd.read_csv(csv_info, encoding = 'shift-jis')
        per_list = df['人数'].to_list()
        per_list = per_list[0:10]
        num = re.sub( r'\D', '', per_person)
        for i in range(len(per_list)):
            per_list[i] = math.ceil(per_list[i]/int(num))
        return render_template('predict.html', ans=res, len=length, day=day, today=tomorrow, per_person=per_person, per_list=per_list)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/comp',methods=['POST'])
def comp():
    print('POSTデータ受け取ったので処理します')
    code1 = request.form['code1']
    code2 = request.form['code2']
    location = request.form['location']

    location_list = []

    code = str(code1) + '-' +str(code2)

    location_list.append(code)
    location_list.append(location)
    loc_csv.main(location_list)
    #weather = gw.main(location_list)
    return render_template('comp.html')

@app.route('/get_weather', methods=['GET'])
def get_weather():
    day = request.args.get('day')
    today = request.args.get('today')
    res = request.args.get('res')
    length = request.args.get('len')
    per_person = request.args.get('per_person')
    per_list = request.args.get('per_list')
    print(per_list)
    with open("controller/static/text/weather.txt", encoding='utf-8') as f:
        content = f.read()

    return render_template('weather.html',content=content,ans=res, len=length, day=day, today=today, per_person=per_person, per_list=per_list)

@app.route('/get_event', methods=['GET'])
def get_event():
    day = request.args.get('day')
    today = request.args.get('today')
    res = request.args.get('res')
    length = request.args.get('len')
    per_person = request.args.get('per_person')
    per_list = request.args.get('per_list')
    with open("controller/static/text/event.txt", encoding='utf-8') as f:
        content = f.read()
    return render_template('events.html', content=content,ans=res, len=length, day=day, today=today, per_person=per_person, per_list=per_list)

@app.route('/home')
def index():
    nowadays = datetime.datetime.now()
    tomorrow = nowadays + datetime.timedelta(1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    return render_template('predict.html', today=tomorrow)


