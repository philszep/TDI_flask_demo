from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.plotting import figure

import pandas as pd 
import numpy as np
import bokeh as bk
import requests
import datetime
import os


app = Flask(__name__)

def make_plot(stock_symbol,AA_key):
  #Get stock data
  stock_ts=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}'.format(stock_symbol,AA_key))
  stock_ts_dict=stock_ts.json()['Time Series (Daily)']
  stock_df = pd.DataFrame.from_dict(stock_ts_dict,orient='index')
  stock_df.index = pd.DatetimeIndex(stock_df.index)

  #Plot in Bokeh
  #output_file("line-test-2.html",mode='inline')
  stock_ser = stock_df['4. close']
  p = figure(title='Stock closing price',x_axis_type='datetime')
  p.line(x=stock_ser.index.date, y=stock_ser.values.astype(float), legend = '{}'.format(stock_symbol))
  
  return p

@app.route('/',methods=['GET','POST'])
def index():

  try: 
    current_stock = request.args.get('stock_symbol',default='GOOG')
  except:
    current_stock = 'GOOG'

  AA_key = os.environ.get('AA_key')
  plot = make_plot(current_stock,AA_key)

  script, div = components(plot)

  return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
  #app.run(debug=True)
  app.run(port=33507)
