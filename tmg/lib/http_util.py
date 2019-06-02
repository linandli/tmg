# -*- coding: utf-8 -*-

"""
对图迹手电服务发送Http请求的封装
"""

import requests
from requests.auth import HTTPBasicAuth
from tglibs.easy_json import o2j
from urllib.parse import urljoin, urlencode

test_server = 'http://115.28.59.161:8080/powerMobileApp/'
publish_server = 'http://115.28.129.229:8080/powerMobileApp/'


class HttpUtil:
    def __init__(self, base_url=test_server, user_name='admin', password='www.togeek.cn', default_timeout=60):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(user_name, password) if all([user_name, password]) else None
        self.session = requests.Session()
        self.http_timeout = default_timeout

    def join_url(self, path):
        return urljoin(self.base_url, '/'.join(map(str, path)))

    @staticmethod
    def handle(response, handler):
        if not response:
            return None, False
        handler = handler or 'raw'
        if handler not in ['text', 'json', 'content', 'raw']:
            raise Exception('无法识别的处理')
        return ((response.json() if handler == 'json' else
                 (response.text if handler == 'text' else
                  (response.content if handler == 'content' else
                   response))),
                response.ok)

    def get(self, path, params=None, timeout=None, handler='json'):
        try:
            timeout = timeout or self.http_timeout
            r = self.session.get(self.join_url(path), params=params, auth=self.auth, timeout=timeout)
            return self.handle(r, handler)
        except:
            return None, False

    def put(self, path, params=None, data=None, timeout=None, handler='json'):
        try:
            timeout = timeout or self.http_timeout
            h = {'Content-Type': 'application/json'}
            r = self.session.put(self.join_url(path), headers=h, params=params,
                                 data=o2j(data, True) if data is not None else data,
                                 auth=self.auth, timeout=timeout)
            return self.handle(r, handler)
        except:
            return None, False

    def post(self, path, params=None, data=None, timeout=None, handler='json'):
        try:
            timeout = timeout or self.http_timeout
            h = {'Content-Type': 'application/json'}
            r = self.session.post(self.join_url(path), headers=h, params=params,
                                  data=o2j(data, True) if data is not None else data,
                                  auth=self.auth, timeout=timeout)
            return self.handle(r, handler)
        except:
            return None, False

    def delete(self, path, params=None, timeout=None, handler='json'):
        try:
            timeout = timeout or self.http_timeout
            r = self.session.delete(self.join_url(path), params=params, auth=self.auth, timeout=timeout)
            return self.handle(r, handler)
        except:
            return None, False

    @staticmethod
    def generate_trans_params(plants, uri, proxy, params):
        plants = [plants] if isinstance(plants, (int, str)) else list(plants)
        result = {'plants': ','.join(map(str, plants))}
        if proxy:
            result['proxy'] = 'true'
        uri = list(uri) if isinstance(uri, (list, tuple)) else [uri]
        result['uri'] = '/%s' % '/'.join(map(str, uri))
        if params:
            result['uri'] += '?%s' % urlencode(params)
        return result

    def trans_get(self, plants, uri, proxy=False, params=None, timeout=None, handler='json'):
        params = self.generate_trans_params(plants, uri, proxy, params)
        return self.get(['distribute', 'trans'], params=params, timeout=timeout, handler=handler)

    def trans_post(self, plants, uri, proxy=False, params=None, data=None, timeout=None, handler='json'):
        params = self.generate_trans_params(plants, uri, proxy, params)
        return self.post(['distribute', 'trans'], params=params, data=data, timeout=timeout, handler=handler)

    def trans_put(self, plants, uri, proxy=False, params=None, data=None, timeout=None, handler='json'):
        params = self.generate_trans_params(plants, uri, proxy, params)
        return self.put(['distribute', 'trans'], params=params, data=data, timeout=timeout, handler=handler)

    def trans_delete(self, plants, uri, proxy=False, params=None, timeout=None, handler='json'):
        params = self.generate_trans_params(plants, uri, proxy, params)
        return self.delete(['distribute', 'trans'], params=params, timeout=timeout, handler=handler)
