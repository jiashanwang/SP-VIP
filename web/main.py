# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify
from common.models import MacOrder, MacUser
from application import db
from application import app
from common.utils import tools, bus
import hashlib, time, jwt, random, requests, json, uuid
from sqlalchemy.sql import text
from common.config.base_config import config

main_page = Blueprint("main", __name__)


@main_page.route("/createOrder", methods=["POST"])
def createOrder():
    '''
    创建支付订单
    '''
    params = request.values.to_dict()
    token_str = request.headers.get('Authorization')
    headers = {
        'content-type': 'application/json',
        "Authorization": token_str
    }
    app_baseurl_url = config.get("app_service_url")
    app_url = app_baseurl_url + "/main/createOrder"
    response_data = requests.post(app_url,
                                  data=json.dumps(params),
                                  headers=headers)
    res_data = json.loads(response_data.text)

    return jsonify(res_data)


@main_page.route("/notifyToApp", methods=["POST"])
def notifyToApp():
    '''
    支付成功的消息回调
    '''
    params = request.json
    print(params)
    pay_time = params.get("payTime")
    ymd = pay_time.split(" ")[0]
    hms = pay_time.split(" ")[1]
    year = int(ymd.split("/")[0])
    month = int(ymd.split("/")[1])
    day = int(ymd.split("/")[2])
    hour = int(hms.split(":")[0])
    minute = int(hms.split(":")[1])
    second = int(hms.split(":")[2])
    curr_seconds = tools.convert_to_seconds(year, month, day, hour, minute, second)
    order_price = float(params.get("amount"))
    order_points = int(float(params.get("amount"))) * 10
    # 1。修改订单支付状态
    mac_order = MacOrder.query.filter(MacOrder.order_code == params.get('outOrderNo')).first()
    mac_order.order_status = 1
    mac_order.order_time = curr_seconds
    mac_order.order_price = order_price
    mac_order.order_points = order_points
    user_id = mac_order.user_id
    db.session.add(mac_order)
    db.session.commit()
    # 2。修改客户积分
    mac_user = MacUser.query.filter(MacUser.user_id == user_id).first()
    mac_user.user_points = mac_user.user_points + order_points
    mac_user.user_end_time = curr_seconds
    user_pid1 = mac_user.user_pid
    user_pid2 = mac_user.user_pid_2
    user_pid3 = mac_user.user_pid_3
    db.session.add(mac_user)
    db.session.commit()
    # 3. 给上级分销商添加对应的推广奖励分 一级奖励50分，二级奖励30分，三级奖励10分
    if user_pid1 > 0:
        # 有一级分销商，则给一级分销商奖励积分
        mac_user1 = MacUser.query.filter(MacUser.user_id == user_pid1).first()
        mac_user1.user_points = mac_user1.user_points + 50
        db.session.add(mac_user1)
        db.session.commit()
        if user_pid2 > 0:
            mac_user2 = MacUser.query.filter(MacUser.user_id == user_pid2).first()
            mac_user2.user_points = mac_user2.user_points + 30
            db.session.add(mac_user2)
            db.session.commit()
            if user_pid3 > 0:
                mac_user3 = MacUser.query.filter(MacUser.user_id == user_pid3).first()
                mac_user3.user_points = mac_user3.user_points + 30
                db.session.add(mac_user3)
                db.session.commit()
    return "success"


@main_page.route("/getVideoUrl", methods=["POST"])
def getVideoUrl():
    '''
    获取视频站点url （从备用池中选择）
    '''
    url_list = ["https://down.meituan.baby", "https://down.jiankun.art", "https://down.liangchaowei.xyz"]
    valid_url = url_list[0]
    for item in url_list:
        app.logger.info("当前url链接==")
        app.logger.info(item)
        is_valid = tools.is_valid_url(item)
        if is_valid:
            # True 有效
            valid_url = item
            break
    app.logger.info("最后返回正确的链接地址为==")
    app.logger.info(valid_url)
    return jsonify(tools.return_data(0, "success", valid_url))
