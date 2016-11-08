#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, url_for, current_app, request
from . import stock
from .. import db
from ..util.get_stock import get_stock
from ..models import User, Stock, User_Stock, Trade
from flask_login import login_required, current_user
from flask_babel import gettext
import tushare as ts, datetime, json



@stock.route('/allstock/')
def allstock():
	whole_indicators = json.loads(ts.get_index().to_json(orient='records'))
	return render_template('stock/all_stock.html',
			whole_indicators=whole_indicators)



@stock.route('/<code>/')
def stock_view(code):
    with current_app.open_resource('stock.json') as f:
        stock_dic = json.loads(f.read())
    name = stock_dic[code]
    DELTA_DAYS = 360
    end = datetime.datetime.now().date()
    start = end - datetime.timedelta(days=DELTA_DAYS)
    stock_data = json.loads(ts.get_hist_data(code=code,start=str(start),end=str(end)).to_json(orient='split'))
    data_days_order = range(len(stock_data['index']))[::-1]
    return render_template('stock/stock_detail.html',
                            title=u'个股详情-'+name,
                            code=code,
                            name=name,
                            stock_data=stock_data,
                            data_days=data_days_order)



@stock.route('/buy/<code>/', methods=['GET', 'POST'])
@login_required
def buy(code):
    #获取股票以及持股关系的实例
    stock = get_stock(code)
    user_stock = User_Stock.query.filter_by(user_id=current_user.id,stock_id=stock.code).first()
    if user_stock == None:
        own_num = 0
    else:
        own_num = user_stock.own_num

    if request.method == 'GET':
        return render_template('stock/trade_buy.html',
                                title=u'股票交易板-'+stock.name,
                                code=code,
                                name=stock.name,
                                balance=current_user.balance,
                                own_num=own_num)

    if request.method == 'POST':
        buy_num = int(request.form['buy_num'])
        price = float(request.form['price'])
        #判断交易能否成功
        if current_user.balance - buy_num * price < 0:
            return render_template('stock/trade_buy.html',
                                    title=u'股票交易板-'+stock.name,
                                    code=code,
                                    name=stock.name,
                                    balance=current_user.balance,
                                    own_num=own_num,
                                    message_done=u'余额不足！')

        #写入交易记录，并更新用户余额
        trade = Trade(user=current_user,stock=stock,num=buy_num,price=price,is_buy=True)
        db.session.add(trade)
        current_user.balance = current_user.balance - price * buy_num
        db.session.commit()

        #更新持股关系
        if user_stock == None:
            user_stock = User_Stock(user=current_user,stock=stock,average_price=price,own_num=0)
            db.session.add(user_stock)
        user_stock.average_price = (user_stock.own_num * user_stock.average_price + buy_num * price) / (user_stock.own_num + buy_num)
        user_stock.own_num = user_stock.own_num + buy_num
        db.session.commit()

        return render_template('stock/trade_buy.html',
                                title=u'股票交易板-'+stock.name,
                                code=code,
                                name=stock.name,
                                balance=current_user.balance,
                                own_num=user_stock.own_num,
                                message_done=u'操作成功！')



@stock.route('/sell/<code>/', methods=['GET', 'POST'])
@login_required
def sell(code):
    #获取股票以及持股关系的实例
    stock = get_stock(code)
    user_stock = User_Stock.query.filter_by(user_id=current_user.id,stock_id=stock.code).first()
    if user_stock == None:
        own_num = 0
    else:
        own_num = user_stock.own_num

    if request.method == 'GET':
        return render_template('stock/trade_sell.html',
                                title=u'股票交易板-'+stock.name,
                                name=stock.name,
                                code=code,
                                balance=current_user.balance,
                                own_num=own_num)

    if request.method == 'POST':
        sell_num = int(request.form['sell_num'])
        price = float(request.form['price'])

        #判断交易是否成功
        if user_stock == None or sell_num > user_stock.own_num:
            return render_template('stock/trade_sell.html',
                                title=u'股票交易板-'+stock.name,
                                name=stock.name,
                                code=code,
                                balance=current_user.balance,
                                own_num=own_num,
                                message_done=u'您的持股数量不足！')

        #写入交易记录，并更新用户余额
        trade = Trade(user=current_user,stock=stock,num=sell_num,price=price,is_buy=False)
        db.session.add(trade)
        current_user.balance = current_user.balance + price * sell_num
        db.session.commit()

        #更新持股关系
        if user_stock.own_num == sell_num:
             user_stock.average_price = 0
             user_stock.own_num = 0
        else:
            user_stock.average_price = (user_stock.own_num * user_stock.average_price - sell_num * price) / (user_stock.own_num - sell_num)
            user_stock.own_num = user_stock.own_num - sell_num
        db.session.commit()

        return render_template('stock/trade_sell.html',
                                title=u'股票交易板-'+stock.name,
                                code=code,
                                name=stock.name,
                                balance=current_user.balance,
                                own_num=user_stock.own_num,
                                message_done=u'操作成功！')




@stock.route('/list/<code>/', methods=['GET', 'POST'])
@login_required
def list(code):
    #获取股票以及持股关系的实例
    stock = get_stock(code)
    trade_list = current_user.trade_list.filter_by(stock_id=code)
    return render_template('stock/trade_list.html',
                            title=u'股票交易清单',
                            code=code,
                            name=stock.name,
                            trade_list=trade_list)



@stock.route('/real/<code>/')
def real_data(code):
     temp = json.loads(ts.get_realtime_quotes(code)[['time','price']].to_json(orient='split'))
     return json.dumps(temp['data'][0])


