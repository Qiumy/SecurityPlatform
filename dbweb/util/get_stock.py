#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from .. import db
from ..models import Stock
import json
def get_stock(code):
    stock = Stock.query.filter_by(code=code).first()
    if stock == None:
        with current_app.open_resource('stock.json') as f:
            stock_dic = json.loads(f.read())
        stock = Stock(code=code,name=stock_dic[code])
        db.session.add(stock)
        db.session.commit()
    return stock