from flask import Flask, request, redirect, send_file
import json, os
from datetime import datetime
#import sensor_graph

# 初期設定　--- (※1)
jsonfile = 'sensor.json'
pngfile = 'sensor.png'
app = Flask(__name__) # Flaskを生成

import os, sys, json, japanize_matplotlib
import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('Agg') # バックエンドに「Agg」に指定 --- (※1)

def draw_graph(data, pngfile):
    # 線グラフを描画するようにデータを分割 --- (※2)
    x, temp, cpu, humi, xx = [],[],[],[],[]
    l_count = int(len(data) / 3)
    for i, row in enumerate(data):
        t = row['time'].split(' ')[1] # 時間
        t2 = t if (i % l_count == 0) else ''
        x.append(i)
        xx.append(t2)
        temp.append(float(row['temp'])) # 温度
        humi.append(float(row['humi'])) # 湿度
        cpu.append(float(row['cpu'])) # CPU温度
    # グラフ上段を描画 --- (※3)
    fig = plt.figure()
    ay1 = fig.add_subplot(2, 1, 1)
    ay1.plot(x, temp, label='温度', linewidth=0.7)
    ay1.plot(x, cpu, label='CPU温度', linewidth=0.7)
    ay1.set_xticks(x)
    ay1.set_xticklabels(xx)
    ay1.legend()
    # グラフ下段を描画 --- (※4)
    ay2 = fig.add_subplot(2, 1, 2)
    ay2.plot(x, humi, label='湿度', linewidth=0.7)
    ay2.set_xticks(x)
    ay2.set_xticklabels(xx)
    ay2.legend()
    plt.savefig(pngfile, dpi=300) # --- (※5)

def draw_file(jsonfile, pngfile):
    # JSONファイルを読む --- (※6)
    if not os.path.exists(jsonfile): return
    with open(jsonfile, encoding='utf-8') as fp:
        data = json.load(fp)
    draw_graph(data, pngfile)


# サーバーのルートにアクセスがあった時 --- (※2)
@app.route('/')
def index():
    return "/save or <a href='/graph'>/graph</a>"

# JSONファイルを元にグラフを描画 --- (※3)
@app.route('/graph')
def graph():
    draw_file(jsonfile, pngfile)
    # 描画したファイルを出力 --- (※4)
    return send_file(pngfile, mimetype='image/png')

# センサーの値を保存する --- (※5)
@app.route('/save')
def save():
    # 投稿されたデータを取得する --- (※6)
    t = request.args.get('t', '') # 温度
    h = request.args.get('h', '') # 湿度
    c = request.args.get('c', '') # CPU温度
    if t == '' or h == '' or c == '': return 'False'
    dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    # 取得した値をJSONに書き込む --- (※7)
    data = []
    if os.path.exists(jsonfile):
        with open(jsonfile, encoding='utf-8') as fp:
            data = json.load(fp)
    data.append({
        'time': dt, 
        'temp': float(t), 
        'humi': float(h),
        'cpu': float(c),
    })
    with open(jsonfile, 'w', encoding='utf-8') as fp:
        json.dump(data, fp)
    return 'True'

if __name__ == '__main__': # サーバー起動 --- (※8)
    app.run(debug=True)

