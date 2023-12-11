# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify
from common.models import AppOrder, AppList, MockOrder
from application import db
from common.utils import tools, bus
import hashlib, time, jwt, random, requests, json, uuid
from sqlalchemy.sql import text
from common.config.base_config import config

main_page = Blueprint("main", __name__)


@main_page.route("/createOrder", methods=["POST"])
def createOrder():
    '''
    创建订单
    接收盘口三个参数：1.订单号 2.支付金额 3. 支付成功的回调地址 4. 支付方式 5. 付款姓名 6。签名参数（服务端请求必须有此字段）
    '''
    params = request.json
    # 先判断订单号是否存在，如果存在，则直接提示订单号重复
    out_order_no = params.get("outOrderNo")  # 盘口传过来的订单号
    exist_order = AppOrder.query.filter(AppOrder.out_order_no == out_order_no).first()
    if exist_order is not None:
        return jsonify(tools.return_data(20, "订单号重复，请刷新页面"))
    authorization = request.headers.get('Authorization')
    token_validate = tools.check_token_validate(authorization)
    if token_validate:
        token = authorization.split()[1]
        pay_method = params.get("payMethod")
        app_data = tools.verify_tokens(token)
        if app_data.get("code") == 0:
            # token 验证成功
            verify_token_data = app_data.get("data").get("data")
            app_id = verify_token_data.get("app_id")  # 盘口app_id
            app_secret = verify_token_data.get("app_secret")  # 盘口app_secret
            if params.get("sign") is not None:
                # 对请求参数生成签名 begin
                out_sign = params.get("sign")  # 盘口传过来的sign签名
                del params['sign']
                sign = tools.generate_sign(params, app_secret)  # 自己的sign签名
                # 盘口服务端请求接口 必须携带sign 字段 ，页面创建订单则不需要传此参数
                if sign != out_sign:
                    # 参数为空或校验失败
                    return jsonify(tools.return_data(1, "签名不正确!"))
            # return "调试代码"
            # 对请求参数生成签名 end
            get_app_data = AppList.query.filter(AppList.app_id == app_id).first()
            # 此处需要判断是微信支付还是支付宝支付【支付渠道：1. 微信H5支付 2. 微信原生支付(二维码 / 链接) 3. 微信小程序支付 4. 微信公众号支付 5. 支付宝H5支付 6.支付宝小程序支付】
            if get_app_data.app_status == "Stop":
                # 商户已经暂停，则直接给提示，不能创建订单
                return jsonify(tools.return_data(1, "商户暂停接单"))
            if pay_method == "wxpay":
                # 创建微信支付码
                payment_type = get_app_data.payment_type_wx
                wx_pay_result = createWxPayCode(payment_type, get_app_data, params, app_id)
                return wx_pay_result
            else:
                # 创建支付宝支付码
                payment_type = get_app_data.payment_type_ali
                ali_pay_result = createAliPayCode(payment_type, get_app_data, params, app_id)
                return ali_pay_result
        else:
            return jsonify(app_data)
    else:
        return jsonify(tools.return_data(1, "token不存在或格式不正确"))


def createWxPayCode(payment_type, get_app_data, params, app_id):
    '''
    创建微信支付码
    '''
    out_order_no = params.get("outOrderNo")  # 盘口传过来的订单号
    amount = params.get("amount")  # 单位元（人民币）
    username = params.get("userName") if params.get("userName") is not None else ""  # 下单用户姓名
    notify_url = params.get("notifyUrl")
    app_name = get_app_data.app_name
    create_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
    order_number = "CF" + str(uuid.uuid4()).replace("-", ''),  # 平台内部订单号
    if len(get_app_data.into_mch_ids_wx) > 0:
        # 手动指定了收款商户
        mch_ids = get_app_data.into_mch_ids_wx.split(";")
        mch_id = random.choice(mch_ids)
        sql = '''
               select payment_types.app_name,payment_types.type,payment_types.appid,payment_types.appsecret,mch_list.mch_id,mch_list.mch_name,
               mch_list.cert_serial_no,mch_list.apiv3 from payment_types,mch_list where payment_types.type=:type and mch_list.mch_id=:mch_id
                and mch_list.mch_id = payment_types.from_mch_id and payment_types.is_delete=1 and mch_list.is_delete=1; 
           '''
        mch_data = db.session.execute(text(sql), {"type": payment_type, "mch_id": mch_id}).fetchall()
        if len(mch_data) > 0:
            mch_list = tools.result_to_dict(mch_data)
            mch_item = random.choice(mch_list)
        else:
            return jsonify(tools.return_data(1, "暂无对应支付渠道"))
    else:
        # 全量使用，从平台商户池中【根据商户选择的支付渠道】
        sql = '''
             select payment_types.app_name,payment_types.type,payment_types.appid,payment_types.appsecret,mch_list.mch_id,mch_list.mch_name,
             mch_list.cert_serial_no,mch_list.apiv3 from payment_types,mch_list where payment_types.type=:type and mch_list.mch_id = payment_types.from_mch_id
             and payment_types.is_delete=1 and mch_list.is_delete=1;
            '''
        mch_data = db.session.execute(text(sql), {"type": payment_type}).fetchall()
        if len(mch_data) > 0:
            mch_list = tools.result_to_dict(mch_data)
            mch_item = random.choice(mch_list)
        else:
            return jsonify(tools.return_data(1, "暂无对应支付渠道"))
    mch_id = mch_item.get("mch_id")
    appid = mch_item.get("appid")
    mch_name = mch_item.get("mch_name")
    appsecret = mch_item.get("appsecret")
    cert_serial_no = mch_item.get("cert_serial_no")
    apiv3 = mch_item.get("apiv3")
    # 1. 创建支付平台的一条订单
    order = AppOrder(username, out_order_no, amount, create_time, notify_url, order_number, "", 0, "",
                     payment_type, app_name, app_id, 0, "", mch_name, mch_id, 1, "")
    db.session.add(order)
    db.session.commit()
    # 2. 创建一条真实订单
    # mock_order = MockOrder("", username, "", amount, 1, create_time, out_order_no, 0, "", "", "", "", "", "", 1, "")
    # db.session.add(mock_order)
    # db.session.commit()
    if order.id is not None:
        # 2. 根据支付类型，调用不同的支付
        app_params = {
            "mch_id": mch_id,
            "appid": appid,
            "appsecret": appsecret,
            "cert_serial_no": cert_serial_no,
            "apiv3": apiv3,
            "out_order_no": out_order_no,
            "amount": amount,
            "create_time": create_time,
        }
        headers = {'content-type': 'application/json'}
        if payment_type == 1:
            # 微信H5支付
            return jsonify(tools.return_data(1, "暂未开放"))
        elif payment_type == 2:
            # 微信原生支付(二维码 / 链接)
            app_baseurl_url = config.get("app_service_url")
            app_url = app_baseurl_url + "/order/unifiedorderOfWxNative"
            response_data = requests.post(app_url,
                                          data=json.dumps(app_params),
                                          headers=headers)
            res_data = json.loads(response_data.text)
            res_data["paymentType"] = payment_type
            return jsonify(tools.return_data(0, "获取成功", res_data))
        elif payment_type == 3:
            # 生成微信小程序的访问链接【微信小程序支付】
            app_baseurl_url = config.get("app_service_url")
            # 方式一： 获取URLLink【小程序链接】begin
            # app_url = app_baseurl_url + "/order/getUrlLink"
            # response_data = requests.post(app_url,
            #                               data=json.dumps(app_params),
            #                               headers=headers)
            # res_data = json.loads(response_data.text)
            # res_data["paymentType"] = payment_type
            # return jsonify(tools.return_data(0, "获取成功", res_data))
            # 获取URLLink【小程序链接】end
            # 方式二： 获取不限制的小程序码【小程序码】begin
            app_url = app_baseurl_url + "/order/getwxacodeunlimit"
            response_data = requests.post(app_url,
                                          data=json.dumps(app_params),
                                          headers=headers)
            res_data = json.loads(response_data.text)
            res_data["paymentType"] = payment_type
            return jsonify(tools.return_data(0, "获取成功", res_data))
            # 获取不限制的小程序码【小程序码】end
        elif payment_type == 4:
            # 微信公众号支付
            return jsonify(tools.return_data(1, "暂未开放"))
        return jsonify(tools.return_data(1, "创建失败"))
    else:
        return jsonify(tools.return_data(1, "创建失败"))


def createAliPayCode(payment_type, get_app_data, params, app_id):
    '''
    创建支付宝支付码
    '''
    out_order_no = params.get("outOrderNo")  # 盘口传过来的订单号
    amount = params.get("amount")  # 单位元（人民币）
    username = params.get("userName") if params.get("userName") is not None else ""  # 下单用户姓名
    notify_url = params.get("notifyUrl")
    app_name = get_app_data.app_name
    create_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
    order_number = "CF" + str(uuid.uuid4()).replace("-", ''),  # 平台内部订单号
    if len(get_app_data.into_mch_ids_ali) > 0:
        # 手动指定了收款商户
        mch_ids = get_app_data.into_mch_ids_ali.split(";")
        mch_id = random.choice(mch_ids)
        sql = '''
               select payment_types.app_name,payment_types.type,payment_types.appid,payment_types.appsecret,mch_list.mch_id,mch_list.mch_name,
               mch_list.cert_serial_no,mch_list.apiv3 from payment_types,mch_list where payment_types.type=:type and mch_list.mch_id=:mch_id
                and mch_list.mch_id = payment_types.from_mch_id and payment_types.is_delete=1 and mch_list.is_delete=1; 
           '''
        mch_data = db.session.execute(text(sql), {"type": payment_type, "mch_id": mch_id}).fetchall()
        if len(mch_data) > 0:
            mch_list = tools.result_to_dict(mch_data)
            mch_item = random.choice(mch_list)
        else:
            return jsonify(tools.return_data(1, "暂无对应支付渠道"))
    else:
        # 全量使用，从平台商户池中【根据商户选择的支付渠道】
        sql = '''
             select payment_types.app_name,payment_types.type,payment_types.appid,payment_types.appsecret,mch_list.mch_id,mch_list.mch_name,
             mch_list.cert_serial_no,mch_list.apiv3 from payment_types,mch_list where payment_types.type=:type and mch_list.mch_id = payment_types.from_mch_id
             and payment_types.is_delete=1 and mch_list.is_delete=1;
            '''
        mch_data = db.session.execute(text(sql), {"type": payment_type}).fetchall()
        if len(mch_data) > 0:
            mch_list = tools.result_to_dict(mch_data)
            mch_item = random.choice(mch_list)
        else:
            return jsonify(tools.return_data(1, "暂无对应支付渠道"))
    appid = mch_item.get("appid")
    mch_id = mch_item.get("mch_id")
    mch_name = mch_item.get("mch_name")
    # 创建支付平台的一条订单
    order = AppOrder(username, out_order_no, amount, create_time, notify_url, order_number, "", 0, "",
                     payment_type, app_name, app_id, 0, "", mch_name, mch_id, 1, "")
    db.session.add(order)
    db.session.commit()
    if order.id is not None:
        # 2. 根据支付类型，调用不同的支付
        app_params = {
            "goodsName": params.get("goodsName"),
            "outOrderNo": out_order_no,
            "amount": amount,
            "notify_url": notify_url,
            "appid": appid,  # 应用APPID
        }
        headers = {'content-type': 'application/json'}
        if payment_type == 5:
            # 支付宝H5支付
            # 方式一：取直接拉起支付链接地址 begin
            # app_baseurl_url = config.get("app_service_url")
            # app_url = app_baseurl_url + "/order/getAliPayObject"
            # response_data = requests.post(app_url,
            #                               data=json.dumps(app_params),
            #                               headers=headers)
            # url = response_data.text
            # res_data = {
            #     "url": url,
            #     "paymentType": payment_type
            # }
            # return jsonify(tools.return_data(0, "创建成功", res_data))
            # 方式一：取直接拉起支付链接地址 end
            # 方式二：返回H5商城链接地址，客户在商城下单 begin
            h5_store_list = ["http://aaa.itgy.com.cn/tinghang/#/", "http://aaa.itgy.com.cn/guosheng/#/"]
            if mch_name == "国昇网络":
                h5_store_url = h5_store_list[1]
            else:
                h5_store_url = h5_store_list[0]
            h5_url = h5_store_url + "?outOrderNo=" + out_order_no
            res_data = {
                "url": h5_url,
                "paymentType": payment_type
            }
            return jsonify(tools.return_data(0, "创建成功", res_data))
            # 方式二：返回H5商城链接地址，客户在商城下单 end
        elif payment_type == 6:
            # 支付宝小程序支付
            return jsonify(tools.return_data(1, "暂未开放"))
        return jsonify(tools.return_data(1, "创建失败"))
    else:
        return jsonify(tools.return_data(1, "创建失败"))


@main_page.route("/getOrderPayState", methods=["POST"])
def getOrderPayState():
    '''
    查询订单支付状态
    '''
    params = request.json
    out_order_no = params.get("outOrderNo")
    authorization = request.headers.get('Authorization')
    token_validate = tools.check_token_validate(authorization)
    if token_validate:
        token = authorization.split()[1]
        app_data = tools.verify_tokens(token)
        if app_data.get("code") == 0:
            # 验证成功
            order_data = AppOrder.query.filter(AppOrder.out_order_no == out_order_no).first()
            if order_data is not None:
                return_data = {
                    "outOrderNo": out_order_no,
                    "payMethod": order_data.payment_type,
                    "payState": order_data.pay_status,
                    "createTime": order_data.create_time,
                    "payTime": order_data.end_time,
                    "amount": order_data.amount,
                    "userName": order_data.username
                }
                return jsonify(tools.return_data(0, "查询成功", return_data))
            else:
                return jsonify(tools.return_data(1, "暂无数据"))
        else:
            return jsonify(app_data)
    else:
        return jsonify(tools.return_data(1, "token不存在或格式不正确"))


@main_page.route("/handNotify", methods=["POST"])
def handNotify():
    '''
    手动回调通知应用订单支付状态，收到回调响应文本"success"
    '''
    params = request.json
    authorization = request.headers.get('Authorization')
    token_validate = tools.check_token_validate(authorization)
    if token_validate:
        token = authorization.split()[1]
        app_data = tools.verify_tokens(token)
        if app_data.get("code") == 0:
            # 验证成功
            app_data = AppOrder.query.filter(AppOrder.out_order_no == params.get("outOrderNo")).first()
            if app_data is not None:
                # 有订单
                notify_url = app_data.notify_url  # 回调地址
                # pay_msg = "支付成功" if app_data.pay_status == 1 else "支付失败"
                if len(notify_url) > 0:
                    # 有回调地址，则通知应用
                    if app_data.pay_status == 1:
                        # 支付成功，可以回调通知
                        app_params = {
                            "payMethod": app_data.payment_type,  # 支付渠道
                            "outOrderNo": app_data.out_order_no,  # 外部订单号
                            "amount": str(app_data.amount),  # 支付金额
                            "payTime": app_data.end_time,  # 支付时间
                            "payStatus": app_data.pay_status,  # 0支付失败 1. 支付成功
                            "payMsg": "支付成功",
                            "userName": app_data.username
                        }
                        headers = {'content-type': 'application/json'}
                        app_notify_url = notify_url
                        response_data = requests.post(app_notify_url,
                                                      data=json.dumps(app_params),
                                                      headers=headers)
                        res_data = response_data.text
                        if res_data == "success":
                            # 通知成功 修改订单的通知状态
                            notify_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
                            app_data.is_notify_to_app = 1
                            app_data.notify_to_app_time = notify_time
                            db.session.add(app_data)
                            db.session.commit()
                            return jsonify(tools.return_data(0, "通知成功"))
                        else:
                            return jsonify(tools.return_data(1, "返回格式有误!"))
                    else:
                        # 未支付/支付失败，则不能回调
                        return jsonify(tools.return_data(1, "订单未支付/支付失败"))
                else:
                    # 无回调地址
                    return jsonify(tools.return_data(1, "无回调地址"))
            else:
                # 订单不存在
                return jsonify(tools.return_data(1, "订单不存在"))
        else:
            return jsonify(app_data)
    else:
        return jsonify(tools.return_data(1, "token不存在或格式不正确"))
