#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from . import main
from flask_babel import gettext
import tushare as ts, json

@main.route('/')
def index():
    whole_indicators = json.loads(ts.get_index()[:4].to_json(orient='records'))
    print whole_indicators
    return render_template('main/index.html',
    						whole_indicators=whole_indicators)


@main.app_errorhandler(404)
def page_404(err):
    return render_template('404.html', title='404'), 404


@main.app_errorhandler(403)
def page_403(err):
    return render_template('403.html', title='403'), 403


@main.app_errorhandler(500)
def page_500(err):
    return render_template('500.html', title='500'), 500
