# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify
from common.models import MacOrder,MacUser
from application import db
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
    测试将支付成功的消息回
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
    mac_order = MacOrder.query.filter(MacOrder.order_code == params.get('outOrderNo')).first()
    mac_order.order_status = 1
    mac_order.order_time = curr_seconds
    mac_order.order_price = order_price
    mac_order.order_points = order_points
    user_id = mac_order.user_id
    db.session.add(mac_order)
    db.session.commit()
    mac_user = MacUser.query.filter(MacUser.user_id == user_id).first()
    mac_user.user_points = mac_user.user_points + order_points
    mac_user.user_end_time = curr_seconds
    db.session.add(mac_user)
    db.session.commit()
    return "success"


@main_page.route("/getRandomVideoList", methods=["POST"])
def getRandomVideoList():
    '''
    从某一个视频分类中，随机抽取几个视频
    '''
    video_list_data = Video.query.filter(Video.from_category == params.get("cateId")).order_by(
        Video.update_time.desc()).paginate(
        page=int(params.get("page")),
        per_page=int(
            params.get("pageSize")),
        error_out=False)
    # # 遍历时要加上items
    video_list = video_list_data.items
    video_result_list = tools.cls_to_dict(video_list)
    if len(video_result_list) > 0:
        return jsonify(tools.return_data(0, "success", video_result_list))
    else:
        return jsonify(tools.return_data(1, "暂无数据"))
