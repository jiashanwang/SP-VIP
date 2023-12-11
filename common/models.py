# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

from application import db


# 创建一个用于将对象转化成json(字典)的类,让每个模型继承这个方法
class EntityBase(object):
    def to_json(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]
        return fields


class Banner(db.Model, EntityBase):
    __tablename__ = 'banner'

    id = db.Column(db.Integer, primary_key=True, info='banner表')
    link = db.Column(db.String(255), server_default=db.FetchedValue(), info='跳转路径')
    src = db.Column(db.String(255), server_default=db.FetchedValue(), info='图片地址')
    from_category = db.Column(db.Integer, server_default=db.FetchedValue(), info='来自于哪个类别下面')

    def __init__(self, link, src, from_category, id=None):
        self.link = link
        self.url = src
        self.from_category = from_category
        if id is not None:
            self.id = id


class Category(db.Model, EntityBase):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, info='分类表')
    name = db.Column(db.String(255), server_default=db.FetchedValue(), info='名称')

    def __init__(self, name, id=None):
        self.name = name
        if id is not None:
            self.id = id


class Video(db.Model, EntityBase):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True, info='ID')
    name = db.Column(db.String(255), server_default=db.FetchedValue(), info='名称')
    poster = db.Column(db.String(255), server_default=db.FetchedValue(), info='封面图片地址')
    src = db.Column(db.String(255), server_default=db.FetchedValue(), info='资源地址')
    update_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='更新时间')
    from_category = db.Column(db.Integer, server_default=db.FetchedValue(), info='分类ID')
    view_nums = db.Column(db.Integer, server_default=db.FetchedValue(), info='浏览次数')

    def __init__(self, name, poster, src, update_time, from_category, view_nums, id=None):
        self.name = name
        self.poster = poster
        self.src = src
        self.update_time = update_time
        self.from_category = from_category
        self.view_nums = view_nums
        if id is not None:
            self.id = id
