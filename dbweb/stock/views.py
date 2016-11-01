#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from . import stock
from flask_babel import gettext
import tushare as ts, datetime
DELTA_DAYS = 180

@stock.route('/<code>')
def index(code):
    end = datetime.datetime.now().date()
    start = end - datetime.timedelta(days=DELTA_DAYS)
    day_data = ts.get_hist_data(code=code,start=str(start),end=str(end))

    return render_template('stock/index.html',
                            title=u'个股详情')