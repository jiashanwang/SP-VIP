# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify
from common.models import Banner, Category, Video
from application import db
from common.utils import tools, bus
import hashlib, time, jwt, random, requests, json, uuid
from sqlalchemy.sql import text
from common.config.base_config import config

main_page = Blueprint("main", __name__)


@main_page.route("/getBannerList", methods=["POST"])
def createOrder():
    '''
    获取分类下的轮播图列表
    '''
    params = request.json
    res_data = Banner.query.filter(Banner.from_category == params.get("cateId")).all()
    if len(res_data) > 0:
        # 当前分类有轮播图
        res_list = tools.cls_to_dict(res_data)
        return jsonify(tools.return_data(0, "success", res_list))
    else:
        return jsonify(tools.return_data(1, "暂无数据"))


@main_page.route("/getCateList", methods=["POST"])
def getCateList():
    '''
    获取所有视频分类
    '''
    cate_data = Category.query.all()
    if len(cate_data) > 0:
        cate_list = tools.cls_to_dict(cate_data)
        return jsonify(tools.return_data(0, "success", cate_list))
    else:
        return jsonify(tools.return_data(1, "暂无数据"))


@main_page.route("/getVideosByCateId", methods=["POST"])
def getVideosByCateId():
    '''
    获取分类的视频
    '''
    params = request.json
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


@main_page.route("/getRandomVideoList", methods=["POST"])
def getRandomVideoList():
    '''
    从某一个视频分类中，随机抽取几个视频
    '''
    params = request.json
    video_data = Video.query.filter(Video.from_category == params.get("cateId")).all()
    if len(video_data) > 0:
        video_list = tools.cls_to_dict(video_data)
        result_list = random.sample(video_list, 6)
        return jsonify(tools.return_data(0, "success", result_list))
    else:
        return jsonify(tools.return_data(1, "暂无数据"))
