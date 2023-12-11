# -*- coding:utf-8 -*-
'''
access_token: 小程序全局唯一后台接口调用凭据
'''
import requests, json, time


class AccessToken:
    '''
    定义获取微信小程序access_token
    '''

    def __init__(self, appid, secret):
        self.appid = appid
        self.appSecret = secret

    def _get_access_token(self):
        url_access_token = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + self.appid + '&secret=' + self.appSecret
        token_res = requests.get(url_access_token)
        token = json.loads(token_res.text).get('access_token')
        return token

    def get_access_token(self):
        url = 'common/config/' + self.appid + '_access_token.conf'
        try:
            with open(url, 'r') as f:
                t, access_token = f.read().split()
        except:
            with open(url, 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7200:
                return access_token
            else:
                with open(url, 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token
