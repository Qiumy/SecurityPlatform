#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from . import main
from flask_babel import gettext
from ..models import Article
import tushare as ts, json
import datetime

@main.route('/')
def index():
    whole_indicators = json.loads(ts.get_index()[:4].to_json(orient='records'))
    whole_news = json.loads(ts.get_latest_news(top=7).to_json(orient="records"))
    notice = Article.query.order_by(Article.updatedTime.desc()).limit(7)

    dates = datetime.datetime.now()
    week = datetime.datetime.now().weekday()
    if week in [5,6]:
        days = 4 - week
        dates = dates + datetime.timedelta(days=days)
    dates = dates.strftime('%Y-%m-%d')

    return render_template('main/index.html',
    						whole_indicators=whole_indicators,
    						news=whole_news,
    						notices=notice,
                            dates = dates)



@main.app_errorhandler(404)
def page_404(err):
    return render_template('404.html', title='404'), 404


@main.app_errorhandler(403)
def page_403(err):
    return render_template('403.html', title='403'), 403


@main.app_errorhandler(500)
def page_500(err):
    return render_template('500.html', title='500'), 500
