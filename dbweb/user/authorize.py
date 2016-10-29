#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect, request, url_for
from flask_login import current_user
from functools import wraps


def user_login(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.signin', next=request.url))
    return wrap


