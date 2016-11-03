#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, url_for, current_app
from . import stock
from flask_babel import gettext
import tushare as ts, datetime, json
DELTA_DAYS = 360

@stock.route('/<code>')
def index(code):
    with current_app.open_resource('stock.json') as f:
        stock_dic = json.loads(f.read())
    
    end = datetime.datetime.now().date()
    start = end - datetime.timedelta(days=DELTA_DAYS)
    stock_data = json.loads(ts.get_hist_data(code=code,start=str(start),end=str(end)).to_json(orient='split'))
    name = stock_dic[code]
    data_days_order = range(len(stock_data['index']))[::-1]

    return render_template('stock/index.html',
                            title=u'个股详情-'+name,
                            code=code,
                            name=name,
                            stock_data=stock_data,
                            data_days=data_days_order)