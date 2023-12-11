# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify
from application import db
from common.utils import tools
from common.models import AppList, AppOrder, UserList, MchList
from sqlalchemy.sql import text

import hashlib, jwt, time, os, requests, json

common_page = Blueprint("common", __name__)


@common_page.route("/getToken", methods=["POST"])
def getToken():
    '''
    生成盘口Token
    '''
    params = request.json
    app_id = params.get("app_id")
    app_secret = params.get("app_secret")
    if app_id is None or app_secret is None:
        return jsonify(tools.return_data(1, "参数有误!"))
    else:
        # 校验appid 和appsecret 是否正确
        app_data = AppList.query.filter(AppList.app_id == app_id, AppList.app_secret == app_secret).first()
        if app_data is not None:
            # 应用后台appid 和密钥存在
            payload = {"app_id": app_id, "app_secret": app_secret}
            token = tools.generate_tokens(payload)
            return jsonify(tools.return_data(0, "获取成功", token))
        else:
            # appid 或 appsecret 有误
            return jsonify(tools.return_data(1, "商户ID或密钥不正确"))


@common_page.route("/notifyToApp", methods=["POST"])
def notifyToApp():
    '''
    测试将支付成功的消息回
    '''
    params = request.json
    return "success"


@common_page.route("/sendEmailTest", methods=["GET"])
def sendEmailTest():
    '''
    测试发送订单邮件
    '''
    send_data = "测试发送订单邮件"
    tools.send_mail(send_data)
    return "200"


@common_page.route("/sendOrderEmailByUser", methods=["GET"])
def sendOrderEmailByUser():
    '''
    给代理和用户发送昨日订单邮件
    代理的邮箱添加到下属所有用户的email 字段里面，多个邮件用分号(;)隔开
    :return:
    '''
    user_data = UserList.query.filter(UserList.is_delete == 1).all()  # 查询所有用户
    title_list = ["订单号", "支付金额(元)", "创建时间", "支付状态", "支付时间", "备注"]
    filed_list = ["out_order_no", "amount", "create_time", "pay_status", "end_time", "remark"]
    user_list = tools.cls_to_dict(user_data)
    if len(user_list) > 0:
        for item in user_list:
            user_id = item.get("id")
            user_name = item.get("user_name")
            emails = item.get("email")
            if len(emails) == 0:
                continue
            if ";" in emails:
                receiver_emails = emails.split(";")
            else:
                receiver_emails = []
                receiver_emails.append(emails)
            # 查询当前用户下面的所有商户号
            mch_data = MchList.query.filter(MchList.from_user_id == user_id, MchList.is_delete == 1).all()
            if len(mch_data) > 0:
                # 当前用户有正在使用中的商户号
                mch_id_list = []
                for mch_item in mch_data:
                    mch_id_list.append(mch_item.mch_id)
                sql_order = '''
                         select * from app_order where TO_DAYS( NOW( ) ) - TO_DAYS(end_time) <= 1 and pay_status = 1 and into_mch_id in ({})
                         '''.format(
                    ','.join(["'%s'" % item for item in mch_id_list]))
                result_order = db.session.execute(text(sql_order)).fetchall()
                if len(result_order) == 0:
                    # 当前用户开通的所有商户号没有订单  不发邮件
                    content = "<html><head></head><body><p> 您好，" + user_name + " : </p><p>昨日无订单数据</p></body></html>"
                    tools.send_mail_annex("", receiver_emails, content, "昨日订单数据")
                else:
                    # 当前用户开通的所有商户号有订单
                    result_order_data = tools.result_to_dict(result_order)
                    xml_order_name = tools.write_xls(title_list, filed_list, result_order_data, user_name)
                    # 文件写入成功后，发邮件
                    content = "<html><head></head><body><p> 您好，" + user_name + " : </p><p>附件为昨日订单数据</p></body></html>"
                    tools.send_mail_annex(xml_order_name, receiver_emails, content, "昨日订单数据", True)

        # 删除当前产生的excel 文件
        files = os.listdir(os.getcwd())
        for file in files:
            if file.endswith(".xls"):
                os.remove(os.path.join(os.getcwd(), file))
        return tools.return_data(0, "订单发送成功")
    else:
        return tools.return_data(1, '当前暂无用户信息')
