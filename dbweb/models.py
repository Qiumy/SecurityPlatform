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
    is_valid_registered = db.Column(db.Boolean, default = False)
    last_login = db.Column(db.DateTime(), default=datetime.utcnow)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    # 权限: 0. 管理员, 1. 普通用户
    permissions = db.Column(db.Integer, default=1, nullable=False)
    website = db.Column(db.String(64), nullable=True)
    avatar_url = db.Column(db.String(64),
                           default="/static/images/default_avatar.jpg")

    # 个人信息, 包括电话号码, 身份证号码, 个人座右铭等。
    telephone = db.Column(db.String(32))
    personal_id = db.Column(db.String(32))
    personal_profile = db.Column(db.Text(), nullable=True)

    # 用户创建话题, 回复等, 一对多的关系
    topics = db.relationship('Topic', backref='user', lazy='dynamic')
    topicNum = db.Column(db.Integer, default=0, nullable=False)

    posts = db.relationship('Post', backref='user', lazy='dynamic')
    postNum = db.Column(db.Integer, default=0, nullable=False)


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


'''互动社区功能'''
class Group(db.Model):
    def __init__(self, title, about):
        self.title = title
        self.about = about
        self.createdTime = datetime.now()

    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)        # 专栏 ID
    title = db.Column(db.String(64), nullable=False)    # 专栏名字
    about = db.Column(db.Text(), nullable=False)        # 专栏介绍
    logo = db.Column(db.String(128))                    # 专栏Logo 的 URL
    topicNum = db.Column(db.Integer, default=0)         # 专栏话题数目
    createdTime = db.Column(db.DateTime(), default=datetime.utcnow)

    # 专栏内的话题，一对多的关系
    topics = db.relationship('Topic', backref='group', lazy='dynamic')

class Topic(db.Model):
    def __init__(self, user_id, title, content, group_id):
        self.userID = user_id
        self.title = title
        self.content = content
        self.time_created = datetime.now()
        self.updatedTime = datetime.now()
        self.groupID = group_id

    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)                # 话题 ID
    title = db.Column(db.String(64), nullable=False)            # 话题标题
    content = db.Column(db.Text(), nullable=False)              # 话题内容
    visitNum = db.Column(db.Integer, default=0)                 # 话题浏览次数
    postNum = db.Column(db.Integer, default=0)                  # 评论次数
    groupID = db.Column(db.Integer, db.ForeignKey('groups.id')) # 所属专栏的ID
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))   # 创建用户的ID

    createdTime = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedTime = db.Column(db.DateTime(), default=datetime.utcnow)

    # 话题的评论，一对多的关系
    posts = db.relationship('Post', backref='topic', lazy='dynamic')


class Post(db.Model):
    def __init__(self, user_id, content):
        self.content = content
        self.userID = user_id
        self.createdTime = datetime.now()

    __tablename = "posts"
    id = db.Column(db.Integer, primary_key=True)                # 评论的ID
    content = db.Column(db.String(1024), nullable=False)        # 评论内容

    topicID = db.Column(db.Integer, db.ForeignKey('topics.id')) # 所属话题的ID
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))   # 回复用户的ID
    createdTime = db.Column(db.DateTime(), default=datetime.utcnow)


""" 咨询信息
@Article: 用来发布站点公告。
"""
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)        # 资讯 ID
    title = db.Column(db.String(64), nullable=False)    # 资讯标题
    content = db.Column(db.Text(), nullable=False)      # 资讯正文
    visitNum = db.Column(db.Integer, default=0)         # 浏览次数

    updatedTime = db.Column(db.DateTime(), default=datetime.utcnow)