# -*- coding:utf-8 -*-
from common.utils.accessToken import AccessToken
import requests, json, random


def get_data_by_key(dict_list, dict_value):
    '''
    根据某一个 key 值 ，找出list列表中key 值相等的字典元素
    '''
    for item in dict_list:
        if item.get("mch_id") == dict_value:
            children = item.get("children")
            app_info = random.choice(children)
            return app_info
