# -*- coding:utf-8 -*-
from application import app

from web.main import main_page
from web.common import common_page
from web.backstage import backstage_page

app.register_blueprint(main_page, url_prefix="/paymentcmj/main")
app.register_blueprint(common_page, url_prefix="/paymentcmj/common")
app.register_blueprint(backstage_page, url_prefix="/paymentcmj/backstage")

