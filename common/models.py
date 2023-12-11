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


class AppList(db.Model, EntityBase):
    __tablename__ = 'app_list'

    id = db.Column(db.Integer, primary_key=True, info='盘口信息表')
    app_id = db.Column(db.String(15), server_default=db.FetchedValue(), info='盘口商户ID')
    app_secret = db.Column(db.String(32), server_default=db.FetchedValue(), info='盘口商户秘钥')
    app_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='商户名称/应用名称')
    app_status = db.Column(db.String(10), server_default=db.FetchedValue(), info='盘口状态\nNormal:正常\nStop:停用')
    platform_point = db.Column(db.Float(3), server_default=db.FetchedValue(), info='平台结算点位')
    create_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='盘口开通时间')
    payment_type_wx = db.Column(db.Integer, server_default=db.FetchedValue(),
                                info='微信支付渠道：\r\n1.微信H5支付\r\n2.微信原生支付(二维码/链接)\r\n3.微信小程序支付\r\n4.微信公众号支付\r\n5.支付宝H5支付\r\n6.支付宝小程序支付\r\n7.微信APP支付\r\n8.支付宝APP支付')
    into_mch_names_wx = db.Column(db.String(255), server_default=db.FetchedValue(),
                                  info='款项进入哪些微信收款商户号名称汇总，不同名称用逗号隔开，为空，则码池的所有商户号都可以使用，不为空，则只有指定的商户号可以收款')
    into_mch_ids_wx = db.Column(db.String(255), server_default=db.FetchedValue(),
                                info='款项进入哪些微信收款商户号ID汇总，不同ID用逗号隔开，为空，则码池的所有商户号都可以使用，不为空，则只有指定的商户号可以收款')
    payment_type_ali = db.Column(db.Integer, server_default=db.FetchedValue(),
                                 info='支付宝支付渠道：\r\n1.微信H5支付\r\n2.微信原生支付(二维码/链接)\r\n3.微信小程序支付\r\n4.微信公众号支付\r\n5.支付宝H5支付\r\n6.支付宝小程序支付\r\n7.微信APP支付\r\n8.支付宝APP支付')
    into_mch_names_ali = db.Column(db.String(255), server_default=db.FetchedValue(),
                                   info='款项进入哪些支付宝收款商户号名称汇总，不同名称用逗号隔开，为空，则码池的所有商户号都可以使用，不为空，则只有指定的商户号可以收款')
    into_mch_ids_ali = db.Column(db.String(255), server_default=db.FetchedValue(),
                                 info='款项进入哪些支付宝收款商户号ID汇总，不同ID用逗号隔开，为空，则码池的所有商户号都可以使用，不为空，则只有指定的商户号可以收款')
    support_methods = db.Column(db.String(100), server_default=db.FetchedValue(),
                                info='商户开通的支付平台类型,wxpay微信 alipay支付宝 开通多个，中间用英文分号;隔开')
    is_delete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除：1(未删除) 2(已删除)')

    def __init__(self, app_id, app_secret, app_name, app_status, platform_point, create_time, payment_type_wx,
                 into_mch_names_wx, into_mch_ids_wx, payment_type_ali, into_mch_names_ali, into_mch_ids_ali,
                 support_methods, is_delete,
                 id=None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_name = app_name
        self.app_status = app_status
        self.platform_point = platform_point
        self.create_time = create_time
        self.payment_type_wx = payment_type_wx
        self.into_mch_names_wx = into_mch_names_wx
        self.into_mch_ids_wx = into_mch_ids_wx
        self.payment_type_ali = payment_type_ali
        self.into_mch_names_ali = into_mch_names_ali
        self.into_mch_ids_ali = into_mch_ids_ali
        self.support_methods = support_methods
        self.is_delete = is_delete
        if id is not None:
            self.id = id


class MchList(db.Model, EntityBase):
    __tablename__ = 'mch_list'

    id = db.Column(db.Integer, primary_key=True, info='收款商户表')
    mch_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='自定义商户号昵称，便于记录')
    mch_id = db.Column(db.String(255), server_default=db.FetchedValue(), info='收款商户号ID')
    cert_serial_no = db.Column(db.String(255), server_default=db.FetchedValue(), info='商户证书序列号')
    apiv3 = db.Column(db.String(255), server_default=db.FetchedValue(), info='商户号的apiv3密钥')
    bank_user_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='开户名（银行卡户主）')
    bank_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='绑定开户银行')
    bank_number = db.Column(db.String(255), server_default=db.FetchedValue(), info='银行卡号')
    bank_address = db.Column(db.String(255), server_default=db.FetchedValue(), info='开户支行')
    create_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='创建时间')
    mch_status = db.Column(db.String(10), server_default=db.FetchedValue(), info='商户号运营状态\nNormal:正常\nStop:停用')
    mch_receive_type = db.Column(db.Integer, server_default=db.FetchedValue(), info='商户号收款类型\n1.对私\n2.对公')
    mch_platform = db.Column(db.String(10), server_default=db.FetchedValue(), info='收款商户号所属平台\nWeChat:微信\nALi:支付宝')
    from_user_id = db.Column(db.Integer, server_default=db.FetchedValue(), info='该商户号来自于哪个用户开通的')
    from_user_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='该商户号来自于哪个用户开通的')
    is_delete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除：1(未删除) 2(已删除)')

    def __init__(self, mch_name, mch_id, cert_serial_no, apiv3, bank_user_name, bank_name, bank_number, bank_address,
                 create_time, mch_status,
                 mch_receive_type, mch_platform, from_user_id, from_user_name, id=None):
        self.mch_name = mch_name
        self.mch_id = mch_id
        self.cert_serial_no = cert_serial_no
        self.apiv3 = apiv3
        self.bank_user_name = bank_user_name
        self.bank_name = bank_name
        self.bank_number = bank_number
        self.bank_address = bank_address
        self.create_time = create_time
        self.mch_status = mch_status
        self.mch_receive_type = mch_receive_type
        self.mch_platform = mch_platform
        self.from_user_id = from_user_id
        self.from_user_name = from_user_name
        if id is not None:
            self.id = id


class AppOrder(db.Model, EntityBase):
    __tablename__ = 'app_order'

    id = db.Column(db.Integer, primary_key=True, info='订单表')
    username = db.Column(db.String(255), server_default=db.FetchedValue(), info='用户名/用户昵称')
    out_order_no = db.Column(db.String(255), server_default=db.FetchedValue(), info='盘口订单号')
    amount = db.Column(db.Numeric(10, 2), server_default=db.FetchedValue(), info='支付金额（元）')
    create_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='订单创建时间')
    notify_url = db.Column(db.String(255), server_default=db.FetchedValue(), info='支付成功的回调地址')
    order_number = db.Column(db.String(255), server_default=db.FetchedValue(), info='系统订单号')
    transaction_id = db.Column(db.String(255), server_default=db.FetchedValue(), info='第三方支付订单号')
    pay_status = db.Column(db.Integer, server_default=db.FetchedValue(),
                           info='订单支付状态：\r\n0:未支付 \r\r\n1:支付成功\r\r\n2:支付失败\r\r\n3:退款中\r\r\n4:已退款 \r\n5.取消订单')
    end_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='订单结束时间')
    payment_type = db.Column(db.Integer, server_default=db.FetchedValue(),
                             info='支付渠道：\r\n1.微信H5支付\r\n2.微信原生支付(二维码/链接)\r\n3.微信小程序支付\r\n4.微信公众号支付\r\n5.支付宝H5支付\r\n6.支付宝小程序支付\r\n7.微信APP支付\r\n8.支付宝APP支付')
    from_app_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='该订单来自于哪个盘口app_name')
    from_app_id = db.Column(db.String(255), server_default=db.FetchedValue(), info='该订单来自于哪个盘口app_id')
    is_notify_to_app = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否已回调通知到盘口\r\n0.未通知\r\n1.已通知')
    notify_to_app_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='回调通知到盘口的时间')
    into_mch_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='款项进入哪个收款商户号昵称')
    into_mch_id = db.Column(db.String(255), server_default=db.FetchedValue(), info='款项进入哪个收款商户号ID')
    is_delete = db.Column(db.Integer, server_default=db.FetchedValue(), info='当前订单是否被删除\r\n1: 未删除\r\n2: 订单已删除')
    remark = db.Column(db.String(255), server_default=db.FetchedValue(), info='订单备注')

    def __init__(self, username, out_order_no, amount, create_time, notify_url, order_number, transaction_id,
                 pay_status,
                 end_time, payment_type, from_app_name, from_app_id, is_notify_to_app,
                 notify_to_app_time, into_mch_name, into_mch_id, is_delete, remark, id=None):
        self.username = username
        self.out_order_no = out_order_no
        self.amount = amount
        self.create_time = create_time
        self.notify_url = notify_url
        self.order_number = order_number
        self.transaction_id = transaction_id
        self.pay_status = pay_status
        self.end_time = end_time
        self.payment_type = payment_type
        self.from_app_name = from_app_name
        self.from_app_id = from_app_id
        self.is_notify_to_app = is_notify_to_app
        self.notify_to_app_time = notify_to_app_time
        self.into_mch_name = into_mch_name
        self.into_mch_id = into_mch_id
        self.is_delete = is_delete
        self.remark = remark
        if id is not None:
            self.id = id


class UserList(db.Model, EntityBase):
    __tablename__ = 'user_list'

    id = db.Column(db.Integer, primary_key=True, info='用户表')
    user_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='用户姓名')
    identification = db.Column(db.Integer, server_default=db.FetchedValue(), info='身份唯一识别码（身份证后6位）')
    payment_point = db.Column(db.Float(3), server_default=db.FetchedValue(), info='结算点位')
    user_role = db.Column(db.String(10), server_default=db.FetchedValue(), info='用户角色\nAgent:代理\nUser:客户')
    create_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='创建时间')
    update_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='更新时间')
    payment_method = db.Column(db.String(255), server_default=db.FetchedValue(),
                               info='结算方式\nWeChat:微信结算 \nAlipay:支付宝结算 \r\nBankCard:银行卡结算')
    wx_account = db.Column(db.String(255), server_default=db.FetchedValue(), info='微信结算账户（微信结算）')
    ali_account = db.Column(db.String(255), server_default=db.FetchedValue(), info='支付宝结算账户（支付宝结算）')
    bank_user_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='开户名（银行卡户主，银行卡结算）')
    bank_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='开户银行（银行卡结算）')
    bank_number = db.Column(db.String(255), server_default=db.FetchedValue(), info='银行卡号（银行卡结算）')
    bank_address = db.Column(db.String(255), server_default=db.FetchedValue(), info='开户支行（银行卡结算）')
    email = db.Column(db.String(255), server_default=db.FetchedValue(), info='用户邮箱（用于接收每日订单）')
    is_delete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除：1(未删除) 2(已删除)')

    def __init__(self, user_name, identification, payment_point, user_role, create_time, update_time,
                 payment_method, wx_account, ali_account, bank_user_name, bank_name, bank_number,
                 bank_address, email, is_delete, id=None):
        self.user_name = user_name
        self.identification = identification
        self.payment_point = payment_point
        self.user_role = user_role
        self.create_time = create_time
        self.update_time = update_time
        self.payment_method = payment_method
        self.wx_account = wx_account
        self.ali_account = ali_account
        self.bank_user_name = bank_user_name
        self.bank_name = bank_name
        self.bank_number = bank_number
        self.bank_address = bank_address
        self.email = email
        self.is_delete = is_delete
        if id is not None:
            self.id = id


class Manager(db.Model, EntityBase):
    __tablename__ = 'manager'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), server_default=db.FetchedValue(), info='用户名')
    password = db.Column(db.String(255), server_default=db.FetchedValue(), info='密码')
    role = db.Column(db.String(255), server_default=db.FetchedValue(),
                     info='超级管理员:administratorSup盘口管理员:appAdmin操作员:operatorAdmin')
    from_appid = db.Column(db.String(15), server_default=db.FetchedValue(), info='盘口APPID')
    is_delete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除：1(未删除) 2(已删除)')

    def __init__(self, username, password, role, from_appid, is_delete, id=None):
        self.username = username
        self.password = password
        self.role = role
        self.from_appid = from_appid
        self.is_delete = is_delete
        if id is not None:
            self.id = id


class PaymentType(db.Model, EntityBase):
    __tablename__ = 'payment_types'

    id = db.Column(db.Integer, primary_key=True, info='支付渠道表')
    app_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='支付渠道名称，如:微信小程序，微信公众号')
    appid = db.Column(db.String(255), server_default=db.FetchedValue(), info='应用id（微信原生native支付appid同微信小程序appid）')
    appsecret = db.Column(db.String(255), server_default=db.FetchedValue(), info='应用密钥')
    from_mch_id = db.Column(db.String(255), server_default=db.FetchedValue(), info='款项进入哪个商户号')
    type = db.Column(db.Integer, server_default=db.FetchedValue(),
                     info='支付渠道：\n1.微信H5支付\n2.微信原生支付(二维码/链接)\n3.微信小程序支付\n4.微信公众号支付\n5.支付宝H5支付\n6.支付宝小程序支付\n7.微信APP支付\n8.支付宝APP支付')
    mch_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='商户号昵称')
    create_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='创建时间')
    is_delete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除：1(未删除) 2(已删除)')

    def __init__(self, app_name, appid, appsecret, from_mch_id, type, mch_name, create_time, id=None):
        self.app_name = app_name
        self.appid = appid
        self.appsecret = appsecret
        self.from_mch_id = from_mch_id
        self.type = type
        self.mch_name = mch_name
        self.create_time = create_time
        if id is not None:
            self.id = id


class ProfitList(db.Model, EntityBase):
    __tablename__ = 'profit_list'

    id = db.Column(db.Integer, primary_key=True, info='id')
    date_ymd = db.Column(db.String(20), server_default=db.FetchedValue(), info='日期-年月日')
    total_amount = db.Column(db.Numeric(10, 2), server_default=db.FetchedValue(), info='当日总流水')
    total_count = db.Column(db.Integer, server_default=db.FetchedValue(), info='当日订单数量')
    from_appid = db.Column(db.String(15), server_default=db.FetchedValue(), info='盘口appid')

    def __init__(self, date_ymd, total_amount, total_count, from_appid='', id=None):
        self.date_ymd = date_ymd
        self.total_amount = total_amount
        self.total_count = total_count
        self.from_appid = from_appid
        if id is not None:
            self.id = id


class MockOrder(db.Model, EntityBase):
    __tablename__ = 'mock_order'

    id = db.Column(db.Integer, primary_key=True, info='小程序真实订单表')
    openid = db.Column(db.String(255), server_default=db.FetchedValue(), info='用户openid')
    user_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='用户名称')
    product_name = db.Column(db.String(255), server_default=db.FetchedValue(), info='商品名称')
    amount = db.Column(db.Numeric(8, 2), server_default=db.FetchedValue(), info='金额')
    buy_no = db.Column(db.Integer, server_default=db.FetchedValue(), info='购买数量')
    create_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='订单创建时间')
    outtradeno = db.Column(db.String(255), server_default=db.FetchedValue(), info='系统订单号')
    pay_state = db.Column(db.Integer, server_default=db.FetchedValue(), info='支付状态0未支付1支付成功')
    pay_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='支付时间')
    uoid = db.Column(db.String(255), server_default=db.FetchedValue(), info='微信/支付宝支付订单号')
    detail_img = db.Column(db.String(255), server_default=db.FetchedValue(), info='商品图片')
    card_no = db.Column(db.String(255), server_default=db.FetchedValue(), info='卡号')
    card_pwd = db.Column(db.String(255), server_default=db.FetchedValue(), info='卡密')
    ship_time = db.Column(db.String(255), server_default=db.FetchedValue(), info='发货时间')
    is_delete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除1未删除2已删除')
    remark = db.Column(db.String(255), server_default=db.FetchedValue(), info='备注')

    def __init__(self, openid, user_name, product_name, amount, buy_no, create_time, outtradeno, pay_state, pay_time,
                 uoid, detail_img, card_no, card_pwd, ship_time, is_delete, remark, id=None):
        self.openid = openid
        self.user_name = user_name
        self.product_name = product_name
        self.amount = amount
        self.buy_no = buy_no
        self.create_time = create_time
        self.outtradeno = outtradeno
        self.pay_state = pay_state
        self.pay_time = pay_time
        self.uoid = uoid
        self.detail_img = detail_img
        self.card_no = card_no
        self.card_pwd = card_pwd
        self.ship_time = ship_time
        self.is_delete = is_delete
        self.remark = remark
        if id is not None:
            self.id = id
