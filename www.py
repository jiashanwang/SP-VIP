# -*- coding:utf-8 -*-
from application import app

from web.main import main_page

app.register_blueprint(main_page, url_prefix="/spvip/main")

