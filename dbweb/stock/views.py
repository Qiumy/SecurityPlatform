#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from . import stock
from flask_babel import gettext
import tushare as ts, json

@stock.route('/')
def index():
    whole_indicators = json.loads(ts.get_index().to_json(orient='records'))
    print whole_indicators
    return render_template('stock/index.html',
    						whole_indicators=whole_indicators)
