# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify
from application import db, app
from common.utils import tools
from common.models import Manager, AppList, AppOrder, UserList, MchList, PaymentType, ProfitList
import time, datetime, random, string, requests, jwt, uuid, bcrypt, json
from sqlalchemy import or_, and_
from sqlalchemy.sql import text
from datetime import date, timedelta
import flask_excel as excel

backstage_page = Blueprint("backstage", __name__)


@app.before_request
def before():
    """
    针对app实例定义全局拦截器 code:0: "成功状态码",1: "错误状态码",10: "签名异常",20: "凭证异常", 21: "登录过期", 30: "无权限", 404: "接口不存在"
    """
    url = request.path
    if "/paymentcmj/backstage" in url:
        # 后台接口请求服务
        if "checkLogin" in url or "downLoadOrders" in url or "getYestodayProfit" in url:
            # 登录页面和订单导出页面 不做token校验，直接放行
            pass
        else:
            # authorization = request.headers.get('Authorization')
            # token_validate = tools.check_token_validate(authorization)
            # if token_validate:
            #     token = authorization.split()[1]
            #     app_data = tools.verify_tokens(token)
            #     if app_data.get("code") == 0:
            #         # token 验证成功则直接放行
            #         pass
            #     else:
            #         return jsonify(app_data)
            # else:
            #     return jsonify(tools.return_data(20, "token不存在或格式不正确"))
            token_str = request.headers.get('Authorization')
            if token_str is not None:
                token_data = tools.verify_tokens(token_str)
                if token_data.get("code") == 0:
                    # token 验证成功则直接放行
                    pass
                else:
                    return jsonify(tools.return_data(20, "凭证异常"))
            else:
                return jsonify(tools.return_data(30, "无权限"))
    else:
        # 其他接口服务直接放行
        pass


@backstage_page.route("/checkLogin", methods=["POST"])
def checkLogin():
    '''
    用户登陆
    '''
    # params = request.json
    # en_str = params.get('password') # 前端加密后的密码
    # pwd = tools.aesDecrypt(en_str)  # 对密码进行解密成明文
    # hashed = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
    # print(hashed)
    # return "200"
    params = request.json
    res = Manager.query.filter(Manager.username == params.get("username")).first()
    en_str = params.get('password')
    pwd = tools.aesDecrypt(en_str)  # 对密码进行解密
    if res is not None:
        # 用户存在
        if bcrypt.checkpw(pwd.encode("utf-8"), res.password.encode("utf-8")):
            data = res.to_json()
            token = tools.generate_tokens(data.get("username"))
            data["token"] = token
            data["role"] = tools.aesEncrypt(data.get("role"))
            return jsonify(tools.return_data(0, "登陆成功", data))
        else:
            return jsonify(tools.return_data(1, "密码不正确"))
    else:
        return jsonify(tools.return_data(1, "用户名不存在"))


@backstage_page.route("/updatePwd", methods=["POST"])
def updatePwd():
    '''
    更新密码
    '''
    params = request.json
    res = Manager.query.filter(Manager.username == params.get("username"),
                               Manager.role == params.get("currRole")).first()
    pwd = params.get("oldPwd")
    if res is not None:
        # 用户存在
        if bcrypt.checkpw(pwd.encode("utf-8"), res.password.encode("utf-8")):
            # 老密码输入正确，开始更新密码
            res.password = bcrypt.hashpw(params.get("newPwd").encode("utf-8"), bcrypt.gensalt())
            db.session.add(res)
            db.session.commit()
            return jsonify(tools.return_data(0, "修改成功"))
        else:
            return jsonify(tools.return_data(1, "密码不正确"))
    else:
        return jsonify(tools.return_data(1, "用户名不正确"))


# ===============================================================================商户管理=========================================================================================

@backstage_page.route("/createApp", methods=["POST"])
def createApp():
    '''
    创建/更新 商户
    '''
    params = request.json
    operate_type = params.get("operateType")  # add 新增 update 修改
    create_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
    support_methods = ";".join(params.get("supportMethods"))
    if operate_type == "add":
        # 新增商户
        app_info = tools.generateAppId()
        check_exist_data = AppList.query.filter(AppList.app_name == params.get("name")).first()
        if check_exist_data is None:
            # 商户不存在，可以新增
            insert_app = AppList(app_info.get("app_id"), app_info.get("app_secret"), params.get("name"),
                                 params.get("state"),
                                 params.get("point"), create_time, 0, "", "", 0, "", "", support_methods, 1)
            db.session.add(insert_app)
            db.session.commit()
            if insert_app.id is not None:
                # 1.创建成功 2.创建盘口后台账号和密码
                check_manager = Manager.query.filter(Manager.username == params.get("username")).first()
                if check_manager is None:
                    # 当前账号不存在，可以创建
                    userpwd = bcrypt.hashpw(params.get("userpwd").encode("utf-8"), bcrypt.gensalt())
                    add_app_user = Manager(params.get("username"), userpwd, "appAdmin", app_info.get("app_id"), 1)
                    db.session.add(add_app_user)
                    db.session.commit()
                    if add_app_user.id is not None:
                        return jsonify(tools.return_data(0, "创建成功", app_info))
                else:
                    AppList.query.filter(AppList.id == insert_app.id).delete()
                    db.session.commit()
                    return jsonify(tools.return_data(1, "用户名(后台)已存在，请修改后再重新创建"))
            else:
                return jsonify(tools.return_data(1, "创建失败"))
        else:
            return jsonify(tools.return_data(1, "商户已存在，不能重复创建"))
    else:
        # 更新商户
        AppList.query.filter(AppList.app_id == params.get("appId")).update(
            {"platform_point": params.get("point"), "support_methods": support_methods,
             "app_status": params.get("state")})
        db.session.commit()
        return jsonify(tools.return_data(0, "更新成功"))


@backstage_page.route("/updateMchInfoOfApp", methods=["POST"])
def updateMchInfoOfApp():
    '''
    更新应用收款商户信息
    '''
    params = request.json
    mchName = params.get("mchName") if params.get("mchName") is not None else ""
    mchId = params.get("mchId") if params.get("mchId") is not None else ""
    if params.get("payMethod") == 1:
        # 修改微信收款设置
        app_data = AppList.query.filter(AppList.app_id == params.get("appId")).first()
        app_data.payment_type_wx = params.get("typeWx")
        app_data.into_mch_names_wx = mchName
        app_data.into_mch_ids_wx = mchId
        db.session.add(app_data)
        db.session.commit()
    else:
        # 修改支付宝微信收款设置
        app_data = AppList.query.filter(AppList.app_id == params.get("appId")).first()
        app_data.payment_type_ali = params.get("typeAli")
        app_data.into_mch_names_ali = mchName
        app_data.into_mch_ids_ali = mchId
        db.session.add(app_data)
        db.session.commit()
    return jsonify(tools.return_data(0, "更新成功"))


@backstage_page.route("/getAppList", methods=["POST"])
def getAppList():
    '''
    获取所有的商户信息
    '''
    params = request.json
    app_state = params.get("appState")
    search_name = params.get("searchName")
    if len(app_state) == 0:
        # 查询所有状态商户（已停用和运营中）
        if len(search_name) == 0:
            # 无关键字查询
            total = AppList.query.filter(AppList.is_delete == 1).count()
            app_list_data = AppList.query.filter(AppList.is_delete == 1).order_by(
                AppList.create_time.desc()).paginate(
                page=int(params.get("page")),
                per_page=int(
                    params.get("pageSize")),
                error_out=False)
            # # 遍历时要加上items
            app_list = app_list_data.items
            app_result_list = tools.cls_to_dict(app_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": app_result_list, "total": total}))
        else:
            # 有关键字查询，优先级最高
            total = AppList.query.filter(AppList.is_delete == 1).filter(
                or_(AppList.app_id == search_name, AppList.app_name == search_name)).count()
            app_list_data = AppList.query.filter(AppList.is_delete == 1).filter(
                or_(AppList.app_id == search_name, AppList.app_name == search_name)).all()
            # # 遍历时要加上items
            app_result_list = tools.cls_to_dict(app_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": app_result_list, "total": total}))
    else:
        # 根据商户运营状态
        if len(search_name) == 0:
            # 无关键字查询
            total = AppList.query.filter(AppList.app_status == app_state, AppList.is_delete == 1).count()
            app_list_data = AppList.query.filter(AppList.app_status == app_state, AppList.is_delete == 1).order_by(
                AppList.create_time.desc()).paginate(page=int(params.get("page")), per_page=int(params.get("pageSize")),
                                                     error_out=False)

            # 遍历时要加上items
            app_list = app_list_data.items
            app_result_list = tools.cls_to_dict(app_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": app_result_list, "total": total}))
        else:
            total = AppList.query.filter(AppList.app_status == app_state, AppList.is_delete == 1).filter(
                or_(AppList.app_id == search_name, AppList.app_name == search_name)).count()
            app_list_data = AppList.query.filter(AppList.app_status == app_state, AppList.is_delete == 1).filter(
                or_(AppList.app_id == search_name, AppList.app_name == search_name)).all()
            app_result_list = tools.cls_to_dict(app_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": app_result_list, "total": total}))


@backstage_page.route("/deleteApp", methods=["POST"])
def deleteApp():
    '''
    删除商户号
    '''
    params = request.json
    app_id = params.get("appId")
    AppList.query.filter(AppList.app_id == app_id).update({"is_delete": 2, "app_status": "Stop"})
    db.session.commit()
    Manager.query.filter(Manager.from_appid == app_id).update({"is_delete": 2})
    db.session.commit()
    return jsonify(tools.return_data(0, "删除成功"))


@backstage_page.route("/getAppInfoData", methods=["POST"])
def getAppInfoData():
    '''
    获取盘口的appid信息
    '''
    params = request.json
    sql = '''
        select app_list.app_id,app_list.app_secret,app_list.support_methods from app_list,manager where app_list.app_id = manager.from_appid and manager.username=:username
    '''
    app_info = db.session.execute(text(sql), {"username": params.get("username")}).fetchone()
    app_data = dict(zip(app_info._fields, app_info._data))
    return jsonify(tools.return_data(0, "获取成功", app_data))


@backstage_page.route("/getSupportMethods", methods=["POST"])
def getSupportMethods():
    '''
    获取盘口开通的支付通道
    '''
    params = request.json
    app_result = AppList.query.filter(AppList.app_id == params.get("appid"), AppList.is_delete == 1).first()
    if app_result is not None:
        support_methods = app_result.support_methods
        return jsonify(tools.return_data(0, "获取成功", support_methods))
    else:
        return jsonify(tools.return_data(1, "应用信息获取失败"))


# ===============================================================================订单管理=========================================================================================

@backstage_page.route("/handNotify", methods=["POST"])
def handNotify():
    '''
    手动回调通知应用订单支付状态，收到回调响应文本"success"
    '''
    params = request.json
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


@backstage_page.route("/getAppOrders", methods=["POST"])
def getAppOrders():
    '''
    获取所有的商户订单
    '''
    params = request.json
    pay_method = params.get("payMethod")
    search_name = params.get("searchName")  # 商户传递过来的第三方订单号
    if pay_method == "":
        # 查询所有支付渠道的订单
        if len(search_name) == 0:
            # 无关键字查询
            total = AppOrder.query.filter(AppOrder.is_delete == 1).count()
            order_list_data = AppOrder.query.filter(AppOrder.is_delete == 1).order_by(
                AppOrder.create_time.desc()).paginate(
                page=int(params.get("page")),
                per_page=int(
                    params.get("pageSize")),
                error_out=False)
            # # 遍历时要加上items
            order_list = order_list_data.items
            order_result_list = tools.cls_to_dict(order_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": order_result_list, "total": total}))
        else:
            # 有关键字查询，优先级最高
            total = AppOrder.query.filter(AppOrder.is_delete == 1).filter(
                or_(AppOrder.from_app_id == search_name, AppOrder.out_order_no == search_name)).count()
            order_list_data = AppOrder.query.filter(AppOrder.is_delete == 1).filter(
                or_(AppOrder.from_app_id == search_name, AppOrder.out_order_no == search_name)).all()
            # # 遍历时要加上items
            order_result_list = tools.cls_to_dict(order_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": order_result_list, "total": total}))
    else:
        # 根据商户运营状态
        if len(search_name) == 0:
            # 无关键字查询
            total = AppOrder.query.filter(AppOrder.payment_type == pay_method, AppOrder.is_delete == 1).count()
            order_list_data = AppOrder.query.filter(AppOrder.payment_type == pay_method,
                                                    AppOrder.is_delete == 1).order_by(
                AppOrder.create_time.desc()).paginate(page=int(params.get("page")),
                                                      per_page=int(params.get("pageSize")),
                                                      error_out=False)

            # 遍历时要加上items
            order_list = order_list_data.items
            order_result_list = tools.cls_to_dict(order_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": order_result_list, "total": total}))
        else:
            total = AppOrder.query.filter(AppOrder.payment_type == pay_method, AppOrder.is_delete == 1).filter(
                or_(AppOrder.from_app_id == search_name, AppOrder.out_order_no == search_name)).count()
            order_list_data = AppOrder.query.filter(AppOrder.payment_type == pay_method,
                                                    AppOrder.is_delete == 1).filter(
                or_(AppOrder.from_app_id == search_name, AppOrder.out_order_no == search_name)).all()
            order_result_list = tools.cls_to_dict(order_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": order_result_list, "total": total}))


@backstage_page.route("/filterAppOrders", methods=["POST"])
def filterAppOrders():
    '''
    获取盘口的订单数据
    '''
    params = request.json
    pay_method = params.get("payMethod")
    search_name = params.get("searchName")  # 商户传递过来的第三方订单号
    appid = params.get("appid")
    if pay_method == "":
        # 查询所有支付渠道的订单
        if len(search_name) == 0:
            # 无关键字查询
            total = AppOrder.query.filter(AppOrder.is_delete == 1, AppOrder.from_app_id == appid).count()
            order_list_data = AppOrder.query.filter(AppOrder.is_delete == 1, AppOrder.from_app_id == appid).order_by(
                AppOrder.create_time.desc()).paginate(
                page=int(params.get("page")),
                per_page=int(
                    params.get("pageSize")),
                error_out=False)
            # # 遍历时要加上items
            order_list = order_list_data.items
            order_result_list = tools.cls_to_dict(order_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": order_result_list, "total": total}))
        else:
            # 有关键字查询，优先级最高
            total = AppOrder.query.filter(AppOrder.is_delete == 1, AppOrder.from_app_id == appid).filter(
                or_(AppOrder.from_app_id == search_name, AppOrder.out_order_no == search_name)).count()
            order_list_data = AppOrder.query.filter(AppOrder.is_delete == 1, AppOrder.from_app_id == appid).filter(
                or_(AppOrder.from_app_id == search_name, AppOrder.out_order_no == search_name)).all()
            # # 遍历时要加上items
            order_result_list = tools.cls_to_dict(order_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": order_result_list, "total": total}))
    else:
        if len(search_name) == 0:
            # 无关键字查询
            total = AppOrder.query.filter(AppOrder.payment_type == pay_method, AppOrder.is_delete == 1,
                                          AppOrder.from_app_id == appid).count()
            order_list_data = AppOrder.query.filter(AppOrder.payment_type == pay_method,
                                                    AppOrder.is_delete == 1, AppOrder.from_app_id == appid).order_by(
                AppOrder.create_time.desc()).paginate(page=int(params.get("page")),
                                                      per_page=int(params.get("pageSize")),
                                                      error_out=False)

            # 遍历时要加上items
            order_list = order_list_data.items
            order_result_list = tools.cls_to_dict(order_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": order_result_list, "total": total}))
        else:
            total = AppOrder.query.filter(AppOrder.payment_type == pay_method, AppOrder.is_delete == 1,
                                          AppOrder.from_app_id == appid).filter(
                or_(AppOrder.from_app_id == search_name, AppOrder.out_order_no == search_name)).count()
            order_list_data = AppOrder.query.filter(AppOrder.payment_type == pay_method,
                                                    AppOrder.is_delete == 1, AppOrder.from_app_id == appid).filter(
                or_(AppOrder.from_app_id == search_name, AppOrder.out_order_no == search_name)).all()
            order_result_list = tools.cls_to_dict(order_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": order_result_list, "total": total}))


@backstage_page.route("/deleteOrder", methods=["POST"])
def deleteOrder():
    '''
    删除订单
    '''
    params = request.json
    order_id = params.get("orderId")
    AppOrder.query.filter(AppOrder.id == order_id).update({"is_delete": 2})
    db.session.commit()
    return jsonify(tools.return_data(0, "删除成功"))


@backstage_page.route("/downLoadOrders", methods=["GET"])
def downLoadOrders():
    '''
    下载订单文件 核对用
    '''
    pay_list = request.args.get('payList')
    begin_time = request.args.get('beginTime')
    end_time = request.args.get('endTime')
    content = [['应用名称', '订单号', '支付金额', '下单时间', '支付时间', '支付状态', '支付渠道']]
    if len(pay_list) == 0:
        # 查询所有订单状态
        if begin_time is None or len(begin_time) == 0:
            # 查询所有
            sql = '''
             select out_order_no,from_app_name,amount,create_time,end_time,pay_status,payment_type,end_time from app_order
            '''
            order_data = db.session.execute(text(sql)).fetchall()
        else:
            # 查询某一个时间范围内的所有状态订单
            sql = '''
            select out_order_no,from_app_name,amount,create_time,end_time,pay_status,payment_type,end_time from app_order where create_time 
            BETWEEN STR_TO_DATE(:begin_time,'%Y-%m-%d %H:%i:%s') AND STR_TO_DATE(:end_time,'%Y-%m-%d %H:%i:%s')
           '''
            order_data = db.session.execute(text(sql), {"begin_time": begin_time, "end_time": end_time}).fetchall()
    else:
        # 查询特定的订单状态
        pay_state = pay_list.split(",")
        if begin_time is None or len(begin_time) == 0:
            # 特定状态的所有订单
            sql = '''
            select out_order_no,from_app_name,amount,create_time,end_time,pay_status,payment_type,end_time from app_order where pay_status in ({})
            '''.format(
                ','.join(["'%s'" % item for item in pay_state]))
            order_data = db.session.execute(text(sql)).fetchall()
        else:
            # 特定状态制定范围内的订单
            sql = '''
              select out_order_no,from_app_name,amount,create_time,end_time,pay_status,payment_type,end_time from app_order where pay_status in ({}) and create_time 
            BETWEEN STR_TO_DATE(:begin_time,'%Y-%m-%d %H:%i:%s') AND STR_TO_DATE(:end_time,'%Y-%m-%d %H:%i:%s')
              '''.format(
                ','.join(["'%s'" % item for item in pay_state]))
            order_data = db.session.execute(sql, {"begin_time": begin_time, "end_time": end_time}).fetchall()
    if len(order_data) > 0:
        order_list = tools.result_to_dict(order_data)
        for item in order_list:
            pay_status = "未支付"
            if item.get("pay_status") == 0:
                pay_status = "未支付"
            elif item.get("pay_status") == 1:
                pay_status = "支付成功"
            elif item.get("pay_status") == 2:
                pay_status = "支付失败"
            elif item.get("pay_status") == 3:
                pay_status = "退款中"
            elif item.get("pay_status") == 4:
                pay_status = "已退款"
            elif item.get("pay_status") == 5:
                pay_status = "取消订单"
            payment_type = "微信原生支付"
            if item.get("payment_type") == 1:
                payment_type = "微信H5支付"
            elif item.get("payment_type") == 2:
                payment_type = "微信原生支付"
            elif item.get("payment_type") == 3:
                payment_type = "微信小程序支付"
            elif item.get("payment_type") == 4:
                payment_type = "微信公众号支付"
            elif item.get("payment_type") == 5:
                payment_type = "支付宝H5支付"
            elif item.get("payment_type") == 6:
                payment_type = "支付宝小程序支付"
            elif item.get("payment_type") == 7:
                payment_type = "微信APP支付"
            elif item.get("payment_type") == 8:
                payment_type = "支付宝APP支付"
            new_content = [item.get("from_app_name"), item.get("out_order_no"), item.get("amount"),
                           item.get("create_time"), item.get("end_time"), pay_status, payment_type]
            content.append(new_content)
        return excel.make_response_from_array(content, "xlsx",
                                              file_name="downloadOrderFile")
    return "暂无数据"


# ===============================================================================用户管理=========================================================================================

@backstage_page.route("/getAllUsers", methods=["POST"])
def getAllUsers():
    '''
    获取所有的用户
    '''
    user_data = UserList.query.filter(UserList.user_role == "User", UserList.is_delete == 1).all()
    user_list = tools.cls_to_dict(user_data)
    return jsonify(tools.return_data(0, "查询成功", user_list))


@backstage_page.route("/createUser", methods=["POST"])
def createUser():
    '''
    创建/更新用户
    '''
    params = request.json
    operate_type = params.get("operateType")  # add 新增 update 修改
    create_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
    if operate_type == "add":
        # 新增商户
        app_info = tools.generateAppId()
        check_exist_data = UserList.query.filter(UserList.identification == params.get("identification")).first()
        if check_exist_data is None:
            # 用户不存在，可以新增
            insert_user = UserList(params.get("name"), params.get("identification"), params.get("point"),
                                   params.get("addUserRole"), create_time,
                                   create_time, params.get("paymentMethod"),
                                   params.get("wxAccount"), params.get("aliAccount"), params.get("bankUserName"),
                                   params.get("bankName"), params.get("bankNumber"), params.get("bankAddress"),
                                   params.get("email"), 1)
            db.session.add(insert_user)
            db.session.commit()
            if insert_user.id is not None:
                # 创建成功
                return jsonify(tools.return_data(0, "创建成功", app_info))
            else:
                return jsonify(tools.return_data(1, "创建失败"))
        else:
            return jsonify(tools.return_data(1, "用户已存在，不能重复创建"))
    else:
        # 更新商户
        AppList.query.filter(AppList.app_id == params.get("appId")).update(
            {"platform_point": params.get("point"), "payment_type": params.get("type"),
             "app_status": params.get("state")})
        db.session.commit()
        return jsonify(tools.return_data(0, "更新成功"))


@backstage_page.route("/getUserList", methods=["POST"])
def getUserList():
    '''
    获取所有的用户信息
    '''
    params = request.json
    user_role = params.get("userRole")
    search_name = params.get("searchName")
    if len(user_role) == 0:
        # 查询所有角色用户（代理/用户）
        if len(search_name) == 0:
            # 无关键字查询
            total = UserList.query.filter(UserList.is_delete == 1).count()
            user_list_data = UserList.query.filter(UserList.is_delete == 1).order_by(
                UserList.create_time.desc()).paginate(
                page=int(params.get("page")),
                per_page=int(
                    params.get("pageSize")),
                error_out=False)
            # # 遍历时要加上items
            user_list = user_list_data.items
            user_result_list = tools.cls_to_dict(user_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": user_result_list, "total": total}))
        else:
            # 有关键字查询，优先级最高
            total = UserList.query.filter(UserList.is_delete == 1).filter(
                or_(UserList.user_name == search_name, UserList.identification == search_name)).count()
            user_list_data = UserList.query.filter(UserList.is_delete == 1).filter(
                or_(UserList.user_name == search_name, UserList.identification == search_name)).all()
            user_result_list = tools.cls_to_dict(user_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": user_result_list, "total": total}))
    else:
        # 根据用户角色
        if len(search_name) == 0:
            # 无关键字查询
            total = UserList.query.filter(UserList.user_role == user_role, UserList.is_delete == 1).count()
            user_list_data = UserList.query.filter(UserList.user_role == user_role, UserList.is_delete == 1).order_by(
                UserList.create_time.desc()).paginate(page=int(params.get("page")),
                                                      per_page=int(params.get("pageSize")),
                                                      error_out=False)

            # 遍历时要加上items
            user_list = user_list_data.items
            user_result_list = tools.cls_to_dict(user_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": user_result_list, "total": total}))
        else:
            total = UserList.query.filter(UserList.user_role == user_role, UserList.is_delete == 1).filter(
                or_(UserList.user_name == search_name, UserList.identification == search_name)).count()
            user_list_data = UserList.query.filter(AppList.user_role == user_role, UserList.is_delete == 1).filter(
                or_(UserList.user_name == search_name, UserList.identification == search_name)).all()
            user_result_list = tools.cls_to_dict(user_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": user_result_list, "total": total}))


@backstage_page.route("/deleteUser", methods=["POST"])
def deleteUser():
    '''
    删除用户
    '''
    params = request.json
    user_id = params.get("userId")
    UserList.query.filter(UserList.id == user_id).update({"is_delete": 2})
    db.session.commit()
    return jsonify(tools.return_data(0, "删除成功"))


# ===============================================================================商户号管理=========================================================================================


@backstage_page.route("/addMchInfo", methods=["POST"])
def addMchInfo():
    '''
    新增商户号
    '''
    params = request.json
    create_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
    # 新增商户号
    check_exist_data = MchList.query.filter(MchList.mch_id == params.get("mch_id"),
                                            MchList.mch_platform == params.get("mch_platform")).first()
    if check_exist_data is None:
        # 商户不存在，可以新增
        insert_mch = MchList(params.get("mch_name"), params.get("mch_id"), params.get("cert_serial_no"),
                             params.get("apiv3"), params.get("bank_user_name"),
                             params.get("bank_name"),
                             params.get("bank_number"), params.get("bank_address"), create_time,
                             params.get("mch_status"), params.get("mch_receive_type"),
                             params.get("mch_platform"), params.get("from_user_id"), params.get("from_user_name"))
        db.session.add(insert_mch)
        db.session.commit()
        if insert_mch.id is not None:
            # 创建成功
            return jsonify(tools.return_data(0, "创建成功"))
        else:
            return jsonify(tools.return_data(1, "创建失败"))
    else:
        return jsonify(tools.return_data(1, "商户号已存在，不能重复创建"))


@backstage_page.route("/getAllMchList", methods=["POST"])
def getAllMchList():
    '''
    获取所有的商户号
    '''
    mch_list_data = MchList.query.all()
    all_mch_list = tools.cls_to_dict(mch_list_data)
    return jsonify(tools.return_data(0, "获取成功", all_mch_list))


@backstage_page.route("/getMchList", methods=["POST"])
def getMchList():
    '''
    获取所有的商户号信息
    '''
    params = request.json
    user_name = str(params.get("userName"))
    search_name = params.get("searchName")
    if len(user_name) == 0:
        # 无用户姓名
        if len(search_name) == 0:
            # 无关键字查询
            total = MchList.query.filter(MchList.is_delete == 1).count()
            mch_list_data = MchList.query.filter(MchList.is_delete == 1).order_by(
                MchList.create_time.desc()).paginate(
                page=int(params.get("page")),
                per_page=int(
                    params.get("pageSize")),
                error_out=False)
            # # 遍历时要加上items
            mch_list = mch_list_data.items
            mch_result_list = tools.cls_to_dict(mch_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": mch_result_list, "total": total}))
        else:
            # 有关键字查询，优先级最高
            total = MchList.query.filter(MchList.mch_id == search_name, MchList.is_delete == 1).count()
            mch_list_data = MchList.query.filter(MchList.mch_id == search_name, MchList.is_delete == 1).all()
            mch_result_list = tools.cls_to_dict(mch_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": mch_result_list, "total": total}))
    else:
        # 根据用户姓名
        if len(search_name) == 0:
            # 无关键字查询
            total = MchList.query.filter(MchList.from_user_id == user_name, MchList.is_delete == 1).count()
            mch_list_data = MchList.query.filter(MchList.from_user_id == user_name, MchList.is_delete == 1).order_by(
                MchList.create_time.desc()).paginate(page=int(params.get("page")),
                                                     per_page=int(params.get("pageSize")), error_out=False)
            # 遍历时要加上items
            mch_list = mch_list_data.items
            mch_result_list = tools.cls_to_dict(mch_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": mch_result_list, "total": total}))
        else:
            total = MchList.query.filter(MchList.from_user_id == user_name, MchList.mch_id == search_name,
                                         MchList.is_delete == 1).count()
            mch_list_data = MchList.query.filter(MchList.from_user_id == user_name, MchList.mch_id == search_name,
                                                 MchList.is_delete == 1).all()
            mch_result_list = tools.cls_to_dict(mch_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": mch_result_list, "total": total}))


@backstage_page.route("/getAllMchIdListOfUser", methods=["POST"])
def getAllMchIdListOfUser():
    '''
    获取所有的用户以及商户号
    '''
    params = request.json
    sql = '''
    select payment_types.app_name,payment_types.type,mch_list.mch_id,mch_list.mch_name,mch_list.from_user_id from payment_types,mch_list 
    where payment_types.type=:type and mch_list.mch_id = payment_types.from_mch_id and mch_list.is_delete = 1;
    '''
    mch_data = db.session.execute(text(sql), {"type": params.get("paymentType")}).fetchall()
    mch_list = tools.result_to_dict(mch_data)
    new_mch_list = tools.delRepeat(mch_list, "mch_id")  # 去重复
    user_data = UserList.query.filter(UserList.is_delete == 1, UserList.user_role == "User").all()
    user_list = tools.cls_to_dict(user_data)  # 所有用户
    # # 创建商户之前，一定会先创建用户和商户号
    all_mchs = []
    for user in user_list:
        user["label"] = user.get("user_name")
        user["value"] = user.get("id")
        user["children"] = []
        for mch in new_mch_list:
            if user.get("id") == mch.get("from_user_id"):
                obj = {
                    "label": mch.get("mch_name"),
                    "value": mch.get("mch_id")
                }
                user["children"].append(obj)
        if len(user["children"]) > 0:
            all_mchs.append(user)
    return jsonify(tools.return_data(0, "获取成功", all_mchs))


@backstage_page.route("/getAppBackData", methods=["POST"])
def getAppBackData():
    '''
    获取应用的后台登录账号和密码
    '''
    params = request.json
    manager_info = Manager.query.filter(Manager.from_appid == params.get("appId")).first()
    if manager_info is not None:
        return_data = {
            "username": manager_info.username,
        }
        return jsonify(tools.return_data(0, "获取成功", return_data))
    return jsonify(tools.return_data(1, "获取失败"))


@backstage_page.route("/changeMchStatus", methods=["POST"])
def changeMchStatus():
    '''
    修改商户号状态
    '''
    params = request.json
    MchList.query.filter(MchList.id == params.get("mchId")).update({"mch_status": params.get("mchStatus")})
    db.session.commit()
    return jsonify(tools.return_data(0, "修改成功"))


@backstage_page.route("/deleteMchById", methods=["POST"])
def deleteMchById():
    '''
    删除商户号
    '''
    params = request.json
    MchList.query.filter(MchList.id == params.get("id")).update({"is_delete": 2})
    db.session.commit()
    return jsonify(tools.return_data(0, "删除成功"))


# ===============================================================================支付渠道管理=========================================================================================
@backstage_page.route("/addPayTypeInfo", methods=["POST"])
def addPayTypeInfo():
    '''
    新增支付渠道
    '''
    params = request.json
    create_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
    check_exist_data = PaymentType.query.filter(PaymentType.appid == params.get("appId"),
                                                PaymentType.type == params.get("type")).first()
    if check_exist_data is None:
        # 渠道不存在，可以新增
        insert_type = PaymentType(params.get("typeName"), params.get("appId"), params.get("appSecret"),
                                  params.get("fromMchId"), params.get("type"), params.get("mchName"), create_time)
        db.session.add(insert_type)
        db.session.commit()
        if insert_type.id is not None:
            # 创建成功
            return jsonify(tools.return_data(0, "新增成功"))
        else:
            return jsonify(tools.return_data(1, "新增失败"))
    else:
        return jsonify(tools.return_data(1, "本渠道已存在，不能重复新增"))


@backstage_page.route("/getPaymentTypeList", methods=["POST"])
def getPaymentTypeList():
    '''
    获取所有的支付渠道列表
    '''
    params = request.json
    type_name = str(params.get("type"))
    search_name = params.get("searchName")
    if len(type_name) == 0:
        # 无支付渠道名称
        if len(search_name) == 0:
            # 无关键字查询
            total = PaymentType.query.filter(PaymentType.is_delete == 1).count()
            type_list_data = PaymentType.query.filter(PaymentType.is_delete == 1).order_by(
                PaymentType.create_time.desc()).paginate(
                page=int(params.get("page")),
                per_page=int(
                    params.get("pageSize")),
                error_out=False)
            # # 遍历时要加上items
            type_list = type_list_data.items
            type_result_list = tools.cls_to_dict(type_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": type_result_list, "total": total}))
        else:
            # 有关键字查询，优先级最高
            total = PaymentType.query.filter(PaymentType.appid == search_name, PaymentType.is_delete == 1).count()
            type_list_data = PaymentType.query.filter(PaymentType.appid == search_name,
                                                      PaymentType.is_delete == 1).all()
            type_result_list = tools.cls_to_dict(type_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": type_result_list, "total": total}))
    else:
        # 根据支付渠道名称
        if len(search_name) == 0:
            # 无关键字查询
            total = PaymentType.query.filter(PaymentType.type == type_name, PaymentType.is_delete == 1).count()
            type_list_data = PaymentType.query.filter(PaymentType.type == type_name,
                                                      PaymentType.is_delete == 1).order_by(
                PaymentType.create_time.desc()).paginate(page=int(params.get("page")),
                                                         per_page=int(params.get("pageSize")), error_out=False)
            # 遍历时要加上items
            type_list = type_list_data.items
            type_result_list = tools.cls_to_dict(type_list)
            return jsonify(tools.return_data(0, "查询成功", {"list": type_result_list, "total": total}))
        else:
            total = PaymentType.query.filter(PaymentType.type == type_name, PaymentType.appid == search_name,
                                             PaymentType.is_delete == 1).count()
            type_list_data = PaymentType.query.filter(PaymentType.type == type_name, PaymentType.appid == search_name,
                                                      PaymentType.is_delete == 1).all()
            type_result_list = tools.cls_to_dict(type_list_data)
            return jsonify(tools.return_data(0, "查询成功", {"list": type_result_list, "total": total}))


@backstage_page.route("/deleteTypeById", methods=["POST"])
def deleteTypeById():
    '''
    删除支付渠道
    '''
    params = request.json
    PaymentType.query.filter(PaymentType.id == params.get("id")).update({"is_delete": 2})
    db.session.commit()
    return jsonify(tools.return_data(0, "删除成功"))


# ===============================================================================销售概况=========================================================================================
@backstage_page.route("/getOrderAndAmount7Days", methods=["POST"])
def getOrderAndAmount7Days():
    '''
     获取最近7天的订单数和销售额
    '''
    params = request.json
    userAesRole = params.get("type")
    user_role = tools.aesDecrypt(userAesRole)  # 对密码进行解密成明文
    if user_role == "administratorSup" or user_role == "operatorAdmin":
        # 查看所有数据
        sql = '''
            select cast(end_time AS date) AS date_list,COUNT(*) AS order_no,SUM(amount) as total_price 
            from app_order where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(end_time) and pay_status=1 GROUP BY cast(end_time AS date)
        '''
        res_data = db.session.execute(text(sql)).fetchall()
    else:
        # 查看当前盘口数据
        sql = '''
          select cast(end_time AS date) AS date_list,COUNT(*) AS order_no,SUM(amount) as total_price 
          from app_order where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(end_time) and pay_status=1 and from_app_id=:from_app_id GROUP BY cast(end_time AS date)
        '''
        res_data = db.session.execute(text(sql), {"from_app_id": params.get("appid")}).fetchall()
    if len(res_data) > 0:
        # 最近7天有订单记录
        order_data_list = tools.result_to_dict(res_data)
        data_list = []
        order_no_list = []
        total_price_list = []
        for item in order_data_list:
            handle_date = str(item.get("date_list").month) + "-" + str(item.get("date_list").day)
            data_list.append(handle_date)
            order_no_list.append(item.get("order_no"))
            total_price_list.append(item.get("total_price"))
        result_data = {
            "data_list": data_list,
            "order_no_list": order_no_list,
            "total_price_list": total_price_list
        }
        return jsonify(tools.return_data(0, "success", result_data))
    else:
        return jsonify(tools.return_data(1, "暂无数据"))


@backstage_page.route("/getOrderBaseInfo", methods=["POST"])
def getOrderBaseInfo():
    '''
    获取订单概况的基本信息（今日订单总数，昨日订单总数，累计订单数）
    '''
    params = request.json
    userAesRole = params.get("type")
    user_role = tools.aesDecrypt(userAesRole)  # 对密码进行解密成明文
    begin_time = "2023-10-05 00:00:00"
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if user_role == "administratorSup" or user_role == "operatorAdmin":
        # 获取所有
        today_total_sql = '''
                  SELECT count(*) as todayTotal from app_order WHERE TO_DAYS(end_time) = TO_DAYS(now()) and pay_status=1;
                 '''
        yestoday_total_sql = '''
                 SELECT count(*) as yestodayTotal FROM app_order WHERE TO_DAYS(NOW()) - TO_DAYS(end_time) = 1 and pay_status=1;
                 '''
        order_total_no_sql = '''
                 SELECT count(*) as orderTotalNo FROM app_order WHERE pay_status = 1 and end_time
                 BETWEEN STR_TO_DATE(:begin_time,'%Y-%m-%d %H:%i:%s') AND STR_TO_DATE(:end_time,'%Y-%m-%d %H:%i:%s');
                 '''
        today_total_data = db.session.execute(text(today_total_sql)).fetchone()
        yestoday_total_data = db.session.execute(text(yestoday_total_sql)).fetchone()
        order_total_no_data = db.session.execute(text(order_total_no_sql),
                                                 {"begin_time": begin_time, "end_time": end_time}).fetchone()
    else:
        # 获取当前盘口
        today_total_sql = '''
                 SELECT count(*) as todayTotal from app_order WHERE TO_DAYS(end_time) = TO_DAYS(now()) and pay_status=1 and from_app_id=:from_app_id;
                '''
        yestoday_total_sql = '''
                SELECT count(*) as yestodayTotal FROM app_order WHERE TO_DAYS(NOW()) - TO_DAYS(end_time) = 1 and pay_status=1 and from_app_id=:from_app_id;
                '''
        order_total_no_sql = '''
                SELECT count(*) as orderTotalNo FROM app_order WHERE pay_status = 1 and end_time
                BETWEEN STR_TO_DATE(:begin_time,'%Y-%m-%d %H:%i:%s') AND STR_TO_DATE(:end_time,'%Y-%m-%d %H:%i:%s') and from_app_id=:from_app_id;
                '''
        today_total_data = db.session.execute(text(today_total_sql), {"from_app_id": params.get("appid")}).fetchone()
        yestoday_total_data = db.session.execute(text(yestoday_total_sql),
                                                 {"from_app_id": params.get("appid")}).fetchone()
        order_total_no_data = db.session.execute(text(order_total_no_sql),
                                                 {"begin_time": begin_time, "end_time": end_time,
                                                  "from_app_id": params.get("appid")}).fetchone()
    today_total_data = dict(zip(today_total_data._fields, today_total_data._data))
    yestoday_total_data = dict(zip(yestoday_total_data._fields, yestoday_total_data._data))
    order_total_no_data = dict(zip(order_total_no_data._fields, order_total_no_data._data))
    res_data = {
        "todayTotal": today_total_data.get("todayTotal"),
        "yestodayTotal": yestoday_total_data.get("yestodayTotal"),
        "orderTotalNo": order_total_no_data.get("orderTotalNo")
    }
    return jsonify(tools.return_data(0, "success", res_data))


@backstage_page.route("/getAmountBaseInfo", methods=["POST"])
def getAmountBaseInfo():
    '''
    获取销售额概况的基本信息（今日销售额，昨日销售额，累计销售额）
    yestodaySalesAmount   todaySalesAmount  salesTotalAmount
    '''
    params = request.json
    userAesRole = params.get("type")
    user_role = tools.aesDecrypt(userAesRole)  # 对密码进行解密成明文
    begin_time = "2023-10-05 00:00:00"
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if user_role == "administratorSup" or user_role == "operatorAdmin":
        # 获取所有
        today_sales_sql = '''
           SELECT SUM(amount) as todaySalesAmount from app_order WHERE TO_DAYS(end_time) = TO_DAYS(now()) and pay_status=1;
           '''
        yestoday_sales_sql = '''
           SELECT SUM(amount) as yestodaySalesAmount FROM app_order WHERE TO_DAYS(NOW()) - TO_DAYS(end_time) = 1 and pay_status=1;
           '''
        order_sales_total_sql = '''
           SELECT SUM(amount) as salesTotalAmount FROM app_order WHERE pay_status = 1 and end_time
        BETWEEN STR_TO_DATE(:begin_time,'%Y-%m-%d %H:%i:%s') AND STR_TO_DATE(:end_time,'%Y-%m-%d %H:%i:%s');
           '''
        today_sales_data = db.session.execute(text(today_sales_sql)).fetchone()
        yestoday_sales_data = db.session.execute(text(yestoday_sales_sql)).fetchone()
        order_sales_total_data = db.session.execute(text(order_sales_total_sql),
                                                    {"begin_time": begin_time, "end_time": end_time}).fetchone()
    else:
        # 获取当前盘口的数据
        today_sales_sql = '''
           SELECT SUM(amount) as todaySalesAmount from app_order WHERE TO_DAYS(end_time) = TO_DAYS(now()) and pay_status=1 and from_app_id=:from_app_id;
           '''
        yestoday_sales_sql = '''
           SELECT SUM(amount) as yestodaySalesAmount FROM app_order WHERE TO_DAYS(NOW()) - TO_DAYS(end_time) = 1 and pay_status=1 and from_app_id=:from_app_id;
           '''
        order_sales_total_sql = '''
           SELECT SUM(amount) as salesTotalAmount FROM app_order WHERE pay_status = 1 and end_time
        BETWEEN STR_TO_DATE(:begin_time,'%Y-%m-%d %H:%i:%s') AND STR_TO_DATE(:end_time,'%Y-%m-%d %H:%i:%s') and from_app_id=:from_app_id;
           '''
        today_sales_data = db.session.execute(text(today_sales_sql), {"from_app_id": params.get("appid")}).fetchone()
        yestoday_sales_data = db.session.execute(text(yestoday_sales_sql),
                                                 {"from_app_id": params.get("appid")}).fetchone()
        order_sales_total_data = db.session.execute(text(order_sales_total_sql),
                                                    {"begin_time": begin_time, "end_time": end_time,
                                                     "from_app_id": params.get("appid")}).fetchone()
    today_sales_data = dict(zip(today_sales_data._fields, today_sales_data._data))
    yestoday_sales_data = dict(zip(yestoday_sales_data._fields, yestoday_sales_data._data))
    order_sales_total_data = dict(zip(order_sales_total_data._fields, order_sales_total_data._data))
    res_data = {
        "todaySalesAmount": today_sales_data.get("todaySalesAmount") if today_sales_data.get(
            "todaySalesAmount") is not None else 0,
        "yestodaySalesAmount": yestoday_sales_data.get("yestodaySalesAmount") if yestoday_sales_data.get(
            "yestodaySalesAmount") is not None else 0,
        "salesTotalAmount": order_sales_total_data.get("salesTotalAmount") if order_sales_total_data.get(
            "salesTotalAmount") is not None else 0
    }
    return jsonify(tools.return_data(0, "success", res_data))


@backstage_page.route("/getAllProfit", methods=["POST"])
def getAllProfit():
    '''
    获取总利润
    pay_state:0 未支付 1 支付成功
    '''
    params = request.json
    begin_time = "2023-10-05 00:00:00"
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if params.get("type") == "today":
        sql = '''
                 SELECT * from app_order WHERE pay_status = 1 and TO_DAYS(end_time)=TO_DAYS(now())
             '''
        res_data = db.session.execute(text(sql)).fetchall()
    elif params.get("type") == "yestoday":
        sql = '''
                SELECT * from app_order WHERE pay_status = 1 and TO_DAYS(NOW()) - TO_DAYS(end_time) = 1
            '''
        res_data = db.session.execute(text(sql)).fetchall()
    elif params.get("type") == "all":
        sql = '''
            SELECT * from app_order WHERE pay_status = 1 and end_time BETWEEN STR_TO_DATE(:begin_time,'%Y-%m-%d %H:%i:%s') AND STR_TO_DATE(:end_time,'%Y-%m-%d %H:%i:%s');
        '''
        res_data = db.session.execute(text(sql), {"begin_time": begin_time, "end_time": end_time}).fetchall()
    total_profit = 0  # 总毛利润
    if len(res_data) > 0:
        result_data = tools.result_to_dict(res_data)
        for item in result_data:
            total_profit = total_profit + float(item.get("amount")) * item.get("platform_point")
    return_data = {
        "total_profit": round(total_profit, 2)
    }
    return jsonify(tools.return_data(0, "success", return_data))


@backstage_page.route("/getYestodayProfitAll", methods=["POST"])
def getYestodayProfitAll():
    '''
    获取昨日总利润(所有盘口)
    pay_state:0 未支付 1 支付成功
    '''
    sql = '''
            SELECT * from app_order WHERE pay_status = 1 and TO_DAYS(NOW()) - TO_DAYS(end_time) = 1
        '''
    res_data = db.session.execute(text(sql)).fetchall()
    total_amount = 0  # 总流水
    if len(res_data) > 0:
        result_data = tools.result_to_dict(res_data)
        for item in result_data:
            total_amount = total_amount + float(item.get("amount"))
        yestoday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        # 定时器查询昨日订单，用于每日利润统计使用 插入新的数据库表中
        count_sql = '''
            SELECT count(*) as totalNumber from app_order WHERE pay_status = 1 and TO_DAYS(NOW()) - TO_DAYS(end_time) = 1
        '''
        count_number = db.session.execute(text(count_sql)).fetchone()
        count_data = dict(zip(count_number._fields, count_number._data))
        total_number = count_data.get("totalNumber")
        insert_profit = ProfitList(yestoday, round(total_amount, 2), total_number)
        db.session.add(insert_profit)
        db.session.commit()
        return jsonify(tools.return_data(0, "success"))
    else:
        return jsonify(tools.return_data(1, "暂无数据"))


@backstage_page.route("/getYestodayProfitApp", methods=["POST"])
def getYestodayProfitApp():
    '''
    获取昨日盘口总利润
    pay_state:0 未支付 1 支付成功
    '''
    # 1。获取所有的盘口号
    result_list = AppList.query.filter(AppList.is_delete == 1).all()
    for app_item in result_list:
        appid = app_item.app_id
        sql = '''
                SELECT * from app_order WHERE pay_status = 1 and from_app_id=:from_app_id and TO_DAYS(NOW()) - TO_DAYS(end_time) = 1 
            '''
        res_data = db.session.execute(text(sql), {"from_app_id": appid}).fetchall()
        total_amount = 0  # 总流水
        if len(res_data) > 0:
            result_data = tools.result_to_dict(res_data)
            for item in result_data:
                total_amount = total_amount + float(item.get("amount"))
            yestoday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
            # 定时器查询昨日订单，用于每日利润统计使用 插入新的数据库表中
            count_sql = '''
                SELECT count(*) as totalNumber from app_order WHERE pay_status = 1 and from_app_id=:from_app_id and TO_DAYS(NOW()) - TO_DAYS(end_time) = 1
            '''
            count_number = db.session.execute(text(count_sql), {"from_app_id": appid}).fetchone()
            count_data = dict(zip(count_number._fields, count_number._data))
            total_number = count_data.get("totalNumber")
            insert_profit = ProfitList(yestoday, round(total_amount, 2), total_number, appid)
            db.session.add(insert_profit)
            db.session.commit()
    return jsonify(tools.return_data(0, "success"))


@backstage_page.route("/getProfitList", methods=["POST"])
def getProfitList():
    '''
    获取每日利润表
    '''
    params = request.json
    userAesRole = params.get("type")
    user_role = tools.aesDecrypt(userAesRole)  # 对密码进行解密成明文
    start = (params.get("pageNo") - 1) * params.get("pageSize")
    end = params.get("pageSize")
    if user_role == "administratorSup" or user_role == "operatorAdmin":
        # 查询所有数据
        sql = '''
           SELECT SQL_CALC_FOUND_ROWS profit_list.* from profit_list where from_appid='' order by id desc LIMIT :start,:end
         '''
        res_data = db.session.execute(text(sql), {"start": start,
                                                  "end": end}).fetchall()
    else:
        # 查询盘口数据
        sql = '''
          SELECT SQL_CALC_FOUND_ROWS profit_list.* from profit_list where from_appid=:from_appid order by id desc LIMIT :start,:end
        '''
        res_data = db.session.execute(text(sql), {"start": start,
                                                  "end": end, "from_appid": params.get("appid")}).fetchall()
    sql1 = "SELECT FOUND_ROWS() as total;"
    res_total = db.session.execute(text(sql1)).fetchone()
    result_total = dict(zip(res_total._fields, res_total._data))
    if len(res_data) > 0:
        result_data = tools.result_to_dict(res_data)
        return_data = {
            "total": result_total.get("total"),
            "data": result_data,
            "pageNo": params.get("pageNo"),
            "pageSize": params.get("pageSize")
        }
        return jsonify(tools.return_data(0, "success", return_data))
    else:
        return jsonify(tools.return_data(0, "暂无数据"))

# ===============================================================================系统管理=========================================================================================
