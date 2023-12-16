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


class MacActor(db.Model, EntityBase):
    __tablename__ = 'mac_actor'

    actor_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    type_id_1 = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    actor_name = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    actor_en = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    actor_alias = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    actor_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    actor_lock = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    actor_letter = db.Column(db.String(1), nullable=False, index=True, server_default=db.FetchedValue())
    actor_sex = db.Column(db.String(1), nullable=False, index=True, server_default=db.FetchedValue())
    actor_color = db.Column(db.String(6), nullable=False, server_default=db.FetchedValue())
    actor_pic = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    actor_blurb = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    actor_remarks = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    actor_area = db.Column(db.String(20), nullable=False, index=True, server_default=db.FetchedValue())
    actor_height = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    actor_weight = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    actor_birthday = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    actor_birtharea = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    actor_blood = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    actor_starsign = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    actor_school = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    actor_works = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    actor_tag = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    actor_class = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    actor_level = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    actor_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    actor_time_add = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    actor_time_hits = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    actor_time_make = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    actor_hits = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    actor_hits_day = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    actor_hits_week = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    actor_hits_month = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    actor_score = db.Column(db.Numeric(3, 1), nullable=False, index=True, server_default=db.FetchedValue())
    actor_score_all = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    actor_score_num = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    actor_up = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    actor_down = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    actor_tpl = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    actor_jumpurl = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    actor_content = db.Column(db.Text, nullable=False)


class MacAdmin(db.Model, EntityBase):
    __tablename__ = 'mac_admin'

    admin_id = db.Column(db.SmallInteger, primary_key=True)
    admin_name = db.Column(db.String(30), nullable=False, index=True, server_default=db.FetchedValue())
    admin_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    admin_random = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    admin_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    admin_auth = db.Column(db.Text, nullable=False)
    admin_login_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    admin_login_ip = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    admin_login_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    admin_last_login_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    admin_last_login_ip = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


class MacAnnex(db.Model, EntityBase):
    __tablename__ = 'mac_annex'

    annex_id = db.Column(db.Integer, primary_key=True)
    annex_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    annex_file = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    annex_size = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    annex_type = db.Column(db.String(8), nullable=False, index=True, server_default=db.FetchedValue())


class MacArt(db.Model, EntityBase):
    __tablename__ = 'mac_art'

    art_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    type_id_1 = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    group_id = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    art_name = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    art_sub = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    art_en = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    art_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    art_letter = db.Column(db.String(1), nullable=False, index=True, server_default=db.FetchedValue())
    art_color = db.Column(db.String(6), nullable=False, server_default=db.FetchedValue())
    art_from = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    art_author = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    art_tag = db.Column(db.String(100), nullable=False, index=True, server_default=db.FetchedValue())
    art_class = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    art_pic = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    art_pic_thumb = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    art_pic_slide = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    art_pic_screenshot = db.Column(db.Text)
    art_blurb = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    art_remarks = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    art_jumpurl = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    art_tpl = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    art_level = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_lock = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_points = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    art_points_detail = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    art_up = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_down = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_hits = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_hits_day = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_hits_week = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_hits_month = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_time_add = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_time_hits = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    art_time_make = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_score = db.Column(db.Numeric(3, 1), nullable=False, index=True, server_default=db.FetchedValue())
    art_score_all = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_score_num = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    art_rel_art = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    art_rel_vod = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    art_pwd = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    art_pwd_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    art_title = db.Column(db.String, nullable=False)
    art_note = db.Column(db.String, nullable=False)
    art_content = db.Column(db.String, nullable=False)


class MacCard(db.Model, EntityBase):
    __tablename__ = 'mac_card'

    card_id = db.Column(db.Integer, primary_key=True)
    card_no = db.Column(db.String(16), nullable=False, index=True, server_default=db.FetchedValue())
    card_pwd = db.Column(db.String(8), nullable=False, index=True, server_default=db.FetchedValue())
    card_money = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    card_points = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    card_use_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    card_sale_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    card_add_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    card_use_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    card_vip = db.Column(db.Integer, nullable=False)
    card_tian = db.Column(db.Integer, nullable=False)


class MacCash(db.Model, EntityBase):
    __tablename__ = 'mac_cash'

    cash_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    cash_status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    cash_points = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    cash_money = db.Column(db.Numeric(12, 2), nullable=False, server_default=db.FetchedValue())
    cash_bank_name = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    cash_bank_no = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    cash_payee_name = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    cash_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    cash_time_audit = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


class MacCjContent(db.Model, EntityBase):
    __tablename__ = 'mac_cj_content'

    id = db.Column(db.Integer, primary_key=True)
    nodeid = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String, nullable=False)


class MacCjHistory(db.Model, EntityBase):
    __tablename__ = 'mac_cj_history'

    md5 = db.Column(db.String(32), primary_key=True, index=True)


class MacCjNode(db.Model, EntityBase):
    __tablename__ = 'mac_cj_node'

    nodeid = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    lastdate = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    sourcecharset = db.Column(db.String(8), nullable=False)
    sourcetype = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    urlpage = db.Column(db.Text, nullable=False)
    pagesize_start = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    pagesize_end = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    page_base = db.Column(db.String(255), nullable=False)
    par_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    url_contain = db.Column(db.String(100), nullable=False)
    url_except = db.Column(db.String(100), nullable=False)
    url_start = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    url_end = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    title_rule = db.Column(db.String(100), nullable=False)
    title_html_rule = db.Column(db.Text, nullable=False)
    type_rule = db.Column(db.String(100), nullable=False)
    type_html_rule = db.Column(db.Text, nullable=False)
    content_rule = db.Column(db.String(100), nullable=False)
    content_html_rule = db.Column(db.Text, nullable=False)
    content_page_start = db.Column(db.String(100), nullable=False)
    content_page_end = db.Column(db.String(100), nullable=False)
    content_page_rule = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    content_page = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    content_nextpage = db.Column(db.String(100), nullable=False)
    down_attachment = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    watermark = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    coll_order = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    customize_config = db.Column(db.Text, nullable=False)
    program_config = db.Column(db.Text, nullable=False)
    mid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


class MacCollect(db.Model, EntityBase):
    __tablename__ = 'mac_collect'

    collect_id = db.Column(db.Integer, primary_key=True)
    collect_name = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    collect_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    collect_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    collect_mid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    collect_appid = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    collect_appkey = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    collect_param = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    collect_filter = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    collect_filter_from = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    collect_opt = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    collect_sync_pic_opt = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(),
                                     info='同步图片选项，0-跟随全局，1-开启，2-关闭')


class MacComment(db.Model, EntityBase):
    __tablename__ = 'mac_comment'

    comment_id = db.Column(db.Integer, primary_key=True)
    comment_mid = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    comment_rid = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    comment_pid = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    comment_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    comment_name = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    comment_ip = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    comment_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    comment_content = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    comment_up = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    comment_down = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    comment_reply = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    comment_report = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


class MacGbook(db.Model, EntityBase):
    __tablename__ = 'mac_gbook'

    gbook_id = db.Column(db.Integer, primary_key=True)
    gbook_rid = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    gbook_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    gbook_name = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    gbook_ip = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    gbook_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    gbook_reply_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    gbook_content = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    gbook_reply = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())


class MacGroup(db.Model, EntityBase):
    __tablename__ = 'mac_group'

    group_id = db.Column(db.SmallInteger, primary_key=True)
    group_name = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    group_status = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    group_type = db.Column(db.Text, nullable=False)
    group_popedom = db.Column(db.Text, nullable=False)
    group_points_day = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    group_points_week = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    group_points_month = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    group_points_year = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    group_points_free = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


class MacLink(db.Model, EntityBase):
    __tablename__ = 'mac_link'

    link_id = db.Column(db.SmallInteger, primary_key=True)
    link_type = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    link_name = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    link_sort = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    link_add_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    link_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    link_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    link_logo = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())


class MacMsg(db.Model, EntityBase):
    __tablename__ = 'mac_msg'

    msg_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    msg_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    msg_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    msg_to = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    msg_code = db.Column(db.String(10), nullable=False, index=True, server_default=db.FetchedValue())
    msg_content = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    msg_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())


class MacOrder(db.Model, EntityBase):
    __tablename__ = 'mac_order'

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    order_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    order_code = db.Column(db.String(30), nullable=False, index=True, server_default=db.FetchedValue())
    order_price = db.Column(db.Numeric(12, 2), nullable=False, server_default=db.FetchedValue())
    order_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    order_points = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    order_pay_type = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    order_pay_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    order_remarks = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    group_time = db.Column(db.String(255))


class MacPlog(db.Model, EntityBase):
    __tablename__ = 'mac_plog'

    plog_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    user_id_1 = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    plog_type = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    plog_points = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    plog_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    plog_remarks = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())


class MacRole(db.Model, EntityBase):
    __tablename__ = 'mac_role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_rid = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    role_name = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    role_en = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    role_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    role_lock = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    role_letter = db.Column(db.String(1), nullable=False, index=True, server_default=db.FetchedValue())
    role_color = db.Column(db.String(6), nullable=False, server_default=db.FetchedValue())
    role_actor = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    role_remarks = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    role_pic = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    role_sort = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    role_level = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    role_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    role_time_add = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    role_time_hits = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    role_time_make = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    role_hits = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    role_hits_day = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    role_hits_week = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    role_hits_month = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    role_score = db.Column(db.Numeric(3, 1), nullable=False, index=True, server_default=db.FetchedValue())
    role_score_all = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    role_score_num = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    role_up = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    role_down = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    role_tpl = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    role_jumpurl = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    role_content = db.Column(db.Text, nullable=False)


# t_mac_tmpvod = db.Table(
#     'mac_tmpvod',
#     db.Column('id1', db.Integer),
#     db.Column('name1', db.String(1024), nullable=False, server_default=db.FetchedValue())
# )
#
# t_mac_tmpwebsite = db.Table(
#     'mac_tmpwebsite',
#     db.Column('id1', db.Integer),
#     db.Column('name1', db.String(1024), nullable=False, server_default=db.FetchedValue())
# )


class MacTopic(db.Model, EntityBase):
    __tablename__ = 'mac_topic'

    topic_id = db.Column(db.SmallInteger, primary_key=True)
    topic_name = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    topic_en = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    topic_sub = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    topic_sort = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    topic_letter = db.Column(db.String(1), nullable=False, server_default=db.FetchedValue())
    topic_color = db.Column(db.String(6), nullable=False, server_default=db.FetchedValue())
    topic_tpl = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    topic_type = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_pic = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_pic_thumb = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_pic_slide = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_key = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_des = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_title = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_blurb = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_remarks = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    topic_level = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_up = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_down = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_score = db.Column(db.Numeric(3, 1), nullable=False, index=True, server_default=db.FetchedValue())
    topic_score_all = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_score_num = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_hits = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_hits_day = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_hits_week = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_hits_month = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_time_add = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_time_hits = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    topic_time_make = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    topic_tag = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    topic_rel_vod = db.Column(db.Text, nullable=False)
    topic_rel_art = db.Column(db.Text, nullable=False)
    topic_content = db.Column(db.Text, nullable=False)
    topic_extend = db.Column(db.Text, nullable=False)


class MacType(db.Model, EntityBase):
    __tablename__ = 'mac_type'

    type_id = db.Column(db.SmallInteger, primary_key=True)
    type_name = db.Column(db.String(60), nullable=False, index=True, server_default=db.FetchedValue())
    type_en = db.Column(db.String(60), nullable=False, index=True, server_default=db.FetchedValue())
    type_sort = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    type_mid = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    type_pid = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    type_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    type_tpl = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    type_tpl_list = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    type_tpl_detail = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    type_tpl_play = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    type_tpl_down = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    type_key = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    type_des = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    type_title = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    type_union = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    type_extend = db.Column(db.Text, nullable=False)
    type_logo = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    type_pic = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    type_jumpurl = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())


class MacUlog(db.Model, EntityBase):
    __tablename__ = 'mac_ulog'

    ulog_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    ulog_mid = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    ulog_type = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    ulog_rid = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    ulog_sid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    ulog_nid = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    ulog_points = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    ulog_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


class MacUser(db.Model, EntityBase):
    __tablename__ = 'mac_user'

    user_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    user_name = db.Column(db.String(30), nullable=False, index=True, server_default=db.FetchedValue())
    user_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    user_nick_name = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    user_qq = db.Column(db.String(16), nullable=False, server_default=db.FetchedValue())
    user_email = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    user_phone = db.Column(db.String(16), nullable=False, server_default=db.FetchedValue())
    user_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_portrait = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    user_portrait_thumb = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    user_openid_qq = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue())
    user_openid_weixin = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue())
    user_question = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    user_answer = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    user_points = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_points_froze = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_reg_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    user_reg_ip = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_login_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_login_ip = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_last_login_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_last_login_ip = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_login_num = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    user_extend = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    user_random = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    user_end_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_pid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_pid_2 = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_pid_3 = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_codes = db.Column(db.String(255), info='0')


class MacVisit(db.Model, EntityBase):
    __tablename__ = 'mac_visit'

    visit_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, server_default=db.FetchedValue())
    visit_ip = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    visit_ly = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    visit_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())


class MacVod(db.Model, EntityBase):
    __tablename__ = 'mac_vod'

    vod_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    type_id_1 = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    group_id = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    vod_name = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    vod_sub = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_en = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    vod_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    vod_letter = db.Column(db.String(1), nullable=False, index=True, server_default=db.FetchedValue())
    vod_color = db.Column(db.String(6), nullable=False, server_default=db.FetchedValue())
    vod_tag = db.Column(db.String(100), nullable=False, index=True, server_default=db.FetchedValue())
    vod_class = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    vod_pic = db.Column(db.String(1024), nullable=False, server_default=db.FetchedValue())
    vod_pic_thumb = db.Column(db.String(1024), nullable=False, server_default=db.FetchedValue())
    vod_pic_slide = db.Column(db.String(1024), nullable=False, server_default=db.FetchedValue())
    vod_pic_screenshot = db.Column(db.Text)
    vod_actor = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    vod_director = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    vod_writer = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    vod_behind = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    vod_blurb = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_remarks = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    vod_pubdate = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    vod_total = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_serial = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    vod_tv = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    vod_weekday = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    vod_area = db.Column(db.String(20), nullable=False, index=True, server_default=db.FetchedValue())
    vod_lang = db.Column(db.String(10), nullable=False, index=True, server_default=db.FetchedValue())
    vod_year = db.Column(db.String(10), nullable=False, index=True, server_default=db.FetchedValue())
    vod_version = db.Column(db.String(30), nullable=False, index=True, server_default=db.FetchedValue())
    vod_state = db.Column(db.String(30), nullable=False, index=True, server_default=db.FetchedValue())
    vod_author = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    vod_jumpurl = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    vod_tpl = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    vod_tpl_play = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    vod_tpl_down = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    vod_isend = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_lock = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_level = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_copyright = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    vod_points = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    vod_points_play = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    vod_points_down = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    vod_hits = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_hits_day = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_hits_week = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_hits_month = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_duration = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    vod_up = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_down = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_score = db.Column(db.Numeric(3, 1), nullable=False, index=True, server_default=db.FetchedValue())
    vod_score_all = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_score_num = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_time_add = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_time_hits = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    vod_time_make = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_trysee = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    vod_douban_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    vod_douban_score = db.Column(db.Numeric(3, 1), nullable=False, server_default=db.FetchedValue())
    vod_reurl = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_rel_vod = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_rel_art = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_pwd = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    vod_pwd_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_pwd_play = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    vod_pwd_play_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_pwd_down = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    vod_pwd_down_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_content = db.Column(db.String, nullable=False)
    vod_play_from = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_play_server = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_play_note = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_play_url = db.Column(db.String, nullable=False)
    vod_down_from = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_down_server = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_down_note = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    vod_down_url = db.Column(db.String, nullable=False)
    vod_plot = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    vod_plot_name = db.Column(db.String, nullable=False)
    vod_plot_detail = db.Column(db.String, nullable=False)


class MacWebsite(db.Model, EntityBase):
    __tablename__ = 'mac_website'

    website_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    type_id_1 = db.Column(db.SmallInteger, nullable=False, index=True, server_default=db.FetchedValue())
    website_name = db.Column(db.String(60), nullable=False, index=True, server_default=db.FetchedValue())
    website_sub = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    website_en = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    website_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    website_letter = db.Column(db.String(1), nullable=False, index=True, server_default=db.FetchedValue())
    website_color = db.Column(db.String(6), nullable=False, server_default=db.FetchedValue())
    website_lock = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_sort = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_jumpurl = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    website_pic = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    website_pic_screenshot = db.Column(db.Text)
    website_logo = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    website_area = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    website_lang = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    website_level = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_time = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_time_add = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_time_hits = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    website_time_make = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_time_referer = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_hits = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_hits_day = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_hits_week = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_hits_month = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_score = db.Column(db.Numeric(3, 1), nullable=False, index=True, server_default=db.FetchedValue())
    website_score_all = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_score_num = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_up = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_down = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_referer = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_referer_day = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_referer_week = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_referer_month = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    website_tag = db.Column(db.String(100), nullable=False, index=True, server_default=db.FetchedValue())
    website_class = db.Column(db.String(255), nullable=False, index=True, server_default=db.FetchedValue())
    website_remarks = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    website_tpl = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    website_blurb = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    website_content = db.Column(db.String, nullable=False)
