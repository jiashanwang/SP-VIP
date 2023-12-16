# -*- coding:utf-8 -*-
from application import app
import www, os,logging
import flask_excel as excel


if __name__ == "__main__":
    # 用于清空日志文件的
    file_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), "zftd_backCode_flask/log.txt")
    if os.path.exists(file_name):
        f = open('log.txt', "r+")
        f.truncate()
    app.debug = False
    handler = logging.FileHandler('log.txt', encoding='UTF-8')
    # handler.setLevel(logging.DEBUG)
    handler.setLevel(logging.INFO)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    excel.init_excel(app)
    app.run(host="0.0.0.0", port=4009)
