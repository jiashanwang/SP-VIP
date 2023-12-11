# -*- coding:utf-8 -*-
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging, os, jwt

db = SQLAlchemy()


class Application(Flask):
    def __init__(self, import_name):
        super().__init__(import_name)
        self.config.from_pyfile("common/config/base_setting.py")
        db.init_app(self)


file_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), "SP-VIP/log.txt")
# 判断文件是否存在，不存在就创建
if not os.path.exists(file_name):
    f = open("log.txt", 'w', encoding="utf-8")
app = Application(__name__)
# 2. 设置允许跨域
CORS(app, resources=r'/*')
