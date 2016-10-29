#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db, login_manager

""" 用户管理模块 """

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)

    is_password_reset_link_valid = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime(), default=datetime.utcnow)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    website = db.Column(db.String(64), nullable=True)
    avatar_url = db.Column(db.String(64),
                           default="/static/images/default_avatar.jpg")

    # 个人信息, 包括电话号码, 身份证号码, 个人座右铭等。
    telephone = db.Column(db.String(32))
    personal_id = db.Column(db.String(32))
    personal_profile = db.Column(db.Text(), nullable=True)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        uid = data.get('id')
        if uid:
            return User.query.get(uid)
        return None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


