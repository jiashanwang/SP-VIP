# -*- coding:utf-8 -*-
from common.config.base_config import config
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from datetime import datetime, timedelta
from jwt import PyJWTError
from base64 import b64encode
from application import app
import hashlib, requests, time, jwt, random, base64, os, smtplib, xlwt
# 发邮件相关依赖包
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 登录页面加解密需要用到以下参数 begin
global key_aes
key_aes = 'atwillpaymentWIN'  # 长度为16的倍数
# SECRET_KEY = os.urandom(16)  # 生成一个随机数作为密钥
JWT_EXPIRY_SECOND = 60 * 60 * 1  # TOKENDE 有效时间，一个小时
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


# 登录页面加解密需要用到 end

def cls_to_dict(cls_list):
    '''
    将数据库查询出来的 <<实例对象>>列表进行统一的转换
    :param cls_list: 待转换的class 实例对象列表
    :return: 字典列表
    '''
    dict_list = []
    for item in cls_list:
        dict_list.append(item.to_json())
    return dict_list


def result_to_dict(result_list):
    '''
    将数据库查询出来的 <<result实例对象>>列表进行统一的转换
    查询结果并不是数据库实例对象（因为字段不完整，是result 对象）
    :param result_list: 待转换的result 实例对象列表
    :return: 字典列表
    '''
    dict_list = []
    for item in result_list:
        dict_list.append(dict(zip(item._fields, item._data)))
    return dict_list


def return_data(code, msg, data=None):
    '''
    response 统一返回格式化
    code:0: "成功状态码",1: "错误状态码",10: "签名异常",20: "凭证异常", 21: "登录过期", 30: "无权限", 404: "接口不存在"
    '''
    if data is not None:
        return {
            "code": code,
            "msg": msg,
            "data": data
        }
    else:
        return {
            "code": code,
            "msg": msg
        }


def encrpt(string, public_key):
    '''
    RSA 加密
    :param string:为待加密的字符串
    :param public_key:为RSA公钥（由微信侧提供）
    :return:
    '''
    rsakey = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(string.encode('utf-8')))
    return cipher_text.decode('utf-8')


def aesEncrypt(data):
    '''
    AES的ECB模式加密方法
    :param key: 密钥
    :param data:被加密字符串（明文）
    :return:密文
    '''
    key = key_aes.encode('utf8')
    # 字符串补位
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf8')
    return enctext


def aesDecrypt(data):
    '''
    :param key: 密钥
    :param data: 加密后的数据（密文）
    :return:明文
    '''
    key = key_aes.encode('utf8')
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 去补位
    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode('utf8')
    # print(text_decrypted)
    return text_decrypted


def day_get(d):
    '''
    　# 获取最近一周的日期
    '''
    for i in range(0, 8):
        oneday = datetime.timedelta(days=i)
        day = d - oneday
        date_to = datetime.datetime(day.year, day.month, day.day)
        yield str(date_to)[5:10]


def generate_sign(param, app_secret):
    '''
    生成签名，对字典进行排序（从小到大）和拼接
    '''
    stringA = ''
    ks = sorted(param.keys())
    # 参数排序
    for k in ks:
        stringA += (k + '=' + str(param[k]) + '&')
    # 拼接商户KEY
    string_sign_temp = stringA + "secret=" + app_secret
    # md5加密,也可以用其他方式
    hash_md5 = hashlib.md5(string_sign_temp.encode('utf8'))
    sign = hash_md5.hexdigest().upper()  # 大写的32位
    # sign = hash_md5.hexdigest().lower()  # 小写的32位
    return sign


def generate_tokens(data):
    '''
    一个用户在一次会话生成一个token
    :param uid: 用户id
    :return:
    '''
    # params：是生成token的参数
    params = {
        'data': data,
        # exp：代表token的有效时间,datetime.utcnow():代表当前时间
        # timedelta:表示转化为毫秒
        # 'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRY_SECOND)
    }
    # key:密钥,
    # algorithm:算法，算法是SHA-256
    # SHA-256:密码散列函数算法.256字节长的哈希值（32个长度的数组）---》16进制字符串表示，长度为64。信息摘要，不可以逆
    secret = config.get("secret_salt")
    return jwt.encode(payload=params, key=secret, algorithm='HS256')


def verify_tokens(token_str):
    '''
    PYJWT 验证token
    :param token_str:如果验证成功返回用户app_id 和app_secret
    '''
    try:
        secret = config.get("secret_salt")
        data = jwt.decode(token_str, secret, algorithms='HS256')
        return return_data(0, "success", data)
    except PyJWTError as e:
        return return_data(20, "Token异常,请重新获取Token")


def delRepeat(data, key):
    '''
    对list 列表里面的字段，根据某一个key 进行去重
    参数data为需要去重的list，key为去重的健（即按照哪个key来去重）
    '''
    new_data = []  # 用于存储去重后的list
    values = []  # 用于存储当前已有的值
    for d in data:
        if d[key] not in values:
            new_data.append(d)
            values.append(d[key])
    return new_data


def get_now_time_yyyymmddhhMMss():
    '''
    获取当前时间的年月日时分秒
    '''
    now_time = datetime.datetime.now()

    # 获取年份
    year_info = str(now_time.year)

    # 获取月份
    month_info = now_time.month
    if month_info and month_info < 10:
        month_info = "0{}".format(str(month_info))
    else:
        month_info = str(month_info)

    # 获取日期
    day_info = now_time.day
    if day_info and day_info < 10:
        day_info = "0{}".format(str(day_info))
    else:
        day_info = str(day_info)
    # 获取小时数
    hour_info = now_time.hour
    if hour_info and hour_info < 10:
        hour_info = "0{}".format(str(hour_info))
    else:
        hour_info = str(hour_info)

    # 获取分钟数
    minute_info = now_time.minute
    if minute_info and minute_info < 10:
        minute_info = "0{}".format(str(minute_info))
    else:
        minute_info = str(minute_info)

    # 获取秒数
    second_info = now_time.second
    if second_info and second_info < 10:
        second_info = "0{}".format(str(second_info))
    else:
        second_info = str(second_info)

    return year_info + month_info + day_info + hour_info + minute_info + second_info


def secondsToYMDHMS(seconds):
    '''
    将秒转化成 年月日 时分秒
    '''
    timeArray = time.localtime(seconds)
    other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return other_style_time


def convert_to_seconds(year, month, day, hour, minute, second):
    '''
    将年月日 时分秒转化成 秒
    '''
    # 创建一个datetime对象
    dt = datetime(year, month, day, hour, minute, second)

    # 计算从1970年1月1日午夜开始的秒数（Unix时间戳）
    seconds_since_epoch = (dt - datetime(1970, 1, 1)).total_seconds()

    return int(seconds_since_epoch)


def generate_random_string(length):
    '''
    生成指定长度的随机字符串（13位是app_id ，32位 是app_screct）
    '''
    # 步骤1: 设置允许获取的字符集合
    characters = "abcdefghijklmnopqrstuvwxyz0123456789"

    # 步骤2: 生成随机索引
    indices = random.sample(range(len(characters)), length)

    # 步骤3: 生成指定长度的字符串
    random_string = ''.join([characters[i] for i in indices])

    # 步骤4: 输出生成的字符串
    return random_string


def get_order_code():
    '''
    生成日期订单号
    年月日时分秒+time.time()的后7位
    '''
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(time.time()).replace('.', '')[-7:])
    return order_no


def check_token_validate(authorization):
    '''
    验证接口请求传递过来的token（正确格式为：Authorization:Bearer+空格+token值）
    1. 请求头是否包含 Authorization 字段
    2. Authorization 的值是否包含：Bearer （划重点：Bearer 后面有一个空格）
    '''
    flag = True
    if authorization is None:
        flag = False
    else:
        if "Bearer " not in authorization:
            flag = False
        else:
            token = authorization.split()[1]
            if token is None:
                flag = False
    return flag


def generateAppId():
    '''
    生成盘口app_id 和 app_secret
    '''
    app_id = generate_random_string(13)
    hash_md5 = hashlib.md5(app_id.encode('utf8'))
    app_secret = hash_md5.hexdigest().lower()  # 小写的32位
    app_data = {
        "app_id": "td" + app_id,  # 长度固定为15位，数据库设定了15位的固定长度
        "app_secret": app_secret
    }
    return app_data


def send_mail(mail_content):
    '''
    发邮件（文本内容）
    mail_content:要发送的邮件正文，html 格式
    receiver_emails：收件人列表 ， list 格式
    '''
    receiver_emails = ["690865953@qq.com"]
    msg = MIMEText(mail_content, 'html', 'utf-8')
    # 两个发件人，随机切换账号，避免同一个邮件发送过多被系统限制  password 是邮箱授权码
    senders = [{"email": "1283305468@qq.com", "password": "kapobpzhnkaehhdc"},
               {"email": "690865953@qq.com", "password": "pbrnwibduavtbege"}]
    current_sender = random.choice(senders)
    sender_email = current_sender.get("email")
    sender_password = current_sender.get("password")

    sender_name = "乐卡甄选"
    # SMTP服务器地址:
    smtp_server = 'smtp.qq.com'
    # 判断收件人是一个还是多个
    receiver_email = receiver_emails[0]

    msg['From'] = formataddr([sender_name, sender_email])  # 发件人邮箱名称、账号
    msg['To'] = receiver_email
    msg['Subject'] = "订单通知"  # 邮件主题
    server = smtplib.SMTP_SSL(smtp_server)  # SMTP协议默认端口是25 centos 7 下发送邮件必须使用 SMTP_SSL
    server.ehlo(smtp_server)  # centos 7 下发送邮件必须使用 ehlo()方法
    server.login(sender_email, sender_password)  # 登陆邮件服务器
    server.sendmail(sender_email, receiver_emails, msg.as_string())
    server.quit()


def send_mail_annex(xml_order_name, receiver_emails, content, title, flag=None):
    '''
    发邮件（带附件）
    name: 邮件接受人的姓名
    xml_order_name:待读取的邮件文件名字
    receiver_emails：邮件接收列表
    flag: True（有订单） ，默认无订单数据
    '''
    if flag is not None:
        msg = MIMEMultipart()
        msg.attach(MIMEText(content, 'html', 'utf-8'))
        with open('./' + xml_order_name, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase('application', 'octet-stream', filename='Yestoday_Total_Order.xls')
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename='Yestoday_Total_Order.xls')
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
    else:
        msg = MIMEText(content, 'html', 'utf-8')
    # 输入Email地址和口令:
    sender_email = "1283305468@qq.com"
    sender_password = "kapobpzhnkaehhdc"
    sender_name = "财易付"
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'
    msg['From'] = formataddr([sender_name, sender_email])  # 发件人邮箱名称、账号
    msg['To'] = ",".join(receiver_emails)
    msg['Subject'] = title
    server = smtplib.SMTP_SSL(smtp_server)  # SMTP协议默认端口是25 centos 7 下发送邮件必须使用 SMTP_SSL
    server.ehlo(smtp_server)  # centos 7 下发送邮件必须使用 ehlo()方法
    server.login(sender_email, sender_password)  # 登陆邮件服务器
    server.sendmail(sender_email, receiver_emails, msg.as_string())
    server.quit()


def write_xls(title_list, filed_list, data_list, user_name):
    '''
    将数据写入 excel 表格
    '''
    i = 0
    work_book = xlwt.Workbook(encoding='utf-8')
    work_sheet = work_book.add_sheet("订单明细")
    first_col0 = work_sheet.col(0)  # xlwt中是行和列都是从0开始计算的
    first_col0.width = 256 * 30
    first_col1 = work_sheet.col(1)
    first_col1.width = 256 * 20
    first_col2 = work_sheet.col(2)
    first_col2.width = 256 * 20
    first_col3 = work_sheet.col(3)
    first_col3.width = 256 * 20
    first_col4 = work_sheet.col(4)
    first_col4.width = 256 * 20
    first_col5 = work_sheet.col(5)
    first_col5.width = 256 * 20
    # font_title 为标题的字体格式
    font_title = xlwt.Font()  # 创建字体样式
    font_title.name = '华文宋体'
    font_title.bold = True
    # 字体颜色
    font_title.colour_index = i
    # 字体大小，18为字号，20为衡量单位
    font_title.height = 20 * 18
    # 自定义文字颜色
    font_title1 = xlwt.Font()  # 创建字体样式
    font_title1.name = '华文宋体'
    font_title1.bold = True
    font_title1.colour_index = 2
    font_title1.height = 20 * 18

    # font_body 为内容的字体央视 默认样式
    font_body = xlwt.Font()
    font_body.name = '华文宋体'
    font_title.colour_index = i
    font_title.height = 20 * 12

    # 设置单元格对齐方式
    alignment = xlwt.Alignment()
    # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
    alignment.horz = 0x02
    # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
    alignment.vert = 0x01
    # 设置自动换行
    alignment.wrap = 1
    # 设置边框
    borders = xlwt.Borders()
    # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
    # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    # 初始化样式 (标题样式)
    style_title = xlwt.XFStyle()
    style_title.font = font_title
    style_title.alignment = alignment
    style_title.borders = borders
    # 初始化样式 (内容样式)
    style_body = xlwt.XFStyle()
    style_body.font = font_body
    style_body.alignment = alignment
    style_body.borders = borders
    # 自定义字体样式
    style_body1 = xlwt.XFStyle()
    style_body1.font = font_title1
    style_body1.alignment = alignment
    style_body1.borders = borders

    # 写入标题
    for index, item in enumerate(title_list):
        work_sheet.write(0, index, item, style_title)
    # 写入内容
    total_price = 0
    for index, item in enumerate(data_list, start=1):
        total_price += float(item.get("amount"))
        if item.get("pay_status") == 1:
            item["pay_status"] = "支付成功"
        for num, val in enumerate(filed_list):
            work_sheet.write(index, num, item.get(val), style_body)
    data_count = len(data_list) + 1
    work_sheet.write(data_count, 0, "累计金额", style_title)
    work_sheet.write(data_count, 1, total_price, style_title)
    curr_date = str(datetime.now()).split(" ")[0] + "-" + str(user_name) + "-order.xls"
    work_book.save(curr_date)
    return curr_date
