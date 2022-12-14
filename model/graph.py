import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import matplotlib as plt

def week_month(df):
    fig= make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df["date"], y=df["売上"], name="売上", line=dict(color="orange")))
    fig.write_image("controller/static/image/graph_earnings.png")
    fig= make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df["date"], y=df["人数"], name="人数", line=dict(color="blue")))
    fig.update_xaxes(title_text="<b>日付<b>")
    fig.update_yaxes(title_text="<b>人数<b>")
    fig.write_html("controller/static/image/graph.html")

def day(df_day):
    fig= make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_day["時間"], y=df_day["売上"], name="売上", line=dict(color="orange")))
    fig.write_image("controller/static/image/graph_earnings.png")
    fig= make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_day["時間"], y=df_day["人数"], name="人数", line=dict(color="blue")))
    fig.update_xaxes(title_text="<b>時間<b>")
    fig.update_yaxes(title_text="<b>人数<b>")
    fig.write_html("controller/static/image/graph.html")


def main(len, day_info):
    day_info = day_info.split('-')
    day_info = str(day_info[1]) + '_' + str(day_info[2])
    print(day_info)
    if(len == '1日'):
        csv_info = 'CSV_files/' + day_info + '_1day.csv'
        df = pd.read_csv(csv_info , encoding = "shift-jis")
        day(df)
    elif(len == '1週間'):
        df = pd.read_csv('CSV_files/9_16_1week.csv' , encoding = "shift-jis")
        #df = df[0:30]
        df['年'] = df['年'].astype(int)
        df['月'] = df['月'].astype(int)
        df['日付'] = df['日付'].astype(int)
        df['date'] = pd.to_datetime({'year': df['年'], 'month': df['月'], 'day': df['日付']})
        week_month(df)
    elif(len=='1か月'):
        df = pd.read_csv('CSV_files/9_16_1month.csv' , encoding = "shift-jis")
        df = df[0:30]
        df['年'] = df['年'].astype(int)
        df['月'] = df['月'].astype(int)
        df['日付'] = df['日付'].astype(int)
        df['date'] = pd.to_datetime({'year': df['年'], 'month': df['月'], 'day': df['日付']})

        week_month(df)