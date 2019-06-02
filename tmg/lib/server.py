# -*- coding: utf-8 -*-

"""
对手电服务常用API的封装
"""

from tglibs.date_time_parser import DateTimeParser
from tglibs.singleton import Singleton
from use_tools.lib.http_util import HttpUtil, test_server, publish_server


class Server(metaclass=Singleton):
    def __init__(self, server_name='test', timeout=600):
        self.http = HttpUtil({'publish': publish_server}.get(server_name, test_server), default_timeout=timeout)
        self.parser = DateTimeParser()

    def get_plants(self):
        """
        获取所有电厂
        :return: [(id, name), ...]
        """
        json, ok = self.http.get(['org', 'plants'])
        return sorted([(item['id'], item['name']) for item in json]) if ok else []

    def get_units(self, plant_id):
        """
        获取电厂机组
        :param plant_id: 电厂Id
        :return: [{'plant_id': , 'plant_name': ,
                   'zone_id': , 'zone_name': ,
                   'unit_id': , 'unit_name': ,
                   'min_power': , 'max_power': }, ...]
        """
        json, ok = self.http.get(['org', 'plants', plant_id, 'units'])
        return json if ok else []

    def get_all_point(self, plant_id):
        """
        获取指定电厂所有点
        :param plant_id: 电厂Id
        :return: [{'id': , 'sisId': , 'plantId': , 'valid': , 'type': , 'description': , 'formula': }, ...]
        """
        json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'config', plant_id, 'define', 'points'],
                                       timeout=600)
        return json.get(str(plant_id), []) if ok else []

    def get_config_by_plant(self, plant_id, re_plant_id=1):
        """
        获取电厂全部配置点
        :param plant_id: 电厂Id
        :param re_plant_id: 如果为示例电厂，则获取一个映射电厂的配置点
        :return: [{'id': , 'sis_id': , 'desc': , 'formula': }, ...]
        """
        plant_id = re_plant_id if plant_id == 10000 else plant_id
        json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'config', plant_id, 'config', 'points'])
        return json.get(str(plant_id), []) if ok else []

    def get_config_by_point(self, plant_id, point_id):
        """
        获取指定点的配置
        :param plant_id: 电厂Id
        :param point_id: 点Id
        :return: {'pointId': , 'desc': , 'formula': } or None
        """
        json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'config', 'configs', point_id])
        return json.get(str(plant_id)) if ok else None

    def insert_config(self, plant_id, point_id, desc, formula):
        """
        插入配置点
        :param plant_id: 电厂Id
        :param point_id: 点Id
        :param desc: 描述
        :param formula: 公式
        :return: True or False
        """
        json, ok = self.http.trans_post(plant_id, ['powerMobileApp', 'config', 'configs'],
                                        data={'pointId': point_id, 'desc': desc, 'formula': formula})
        return json.get(str(plant_id), False) if ok else False

    def delete_config(self, plant_id, point_id):
        """
        删除配置点
        :param plant_id: 电厂Id
        :param point_id: 点Id
        :return: True or False
        """
        json, ok = self.http.trans_delete(plant_id, ['powerMobileApp', 'config', 'configs', point_id])
        return json.get(str(plant_id), False) if ok else False

    def update_config(self, plant_id, point_id, desc, formula):
        """
        更新配置点
        :param plant_id: 电厂Id
        :param point_id: 点Id
        :param desc: 描述
        :param formula: 公式
        :return: True or False
        """
        json, ok = self.http.trans_put(plant_id, ['powerMobileApp', 'config', 'configs'],
                                       data={'pointId': point_id, 'desc': desc, 'formula': formula})
        return json.get(str(plant_id), False) if ok else False

    def insert_calc_point(self, plant_id, desc, formula):
        """
        插入新的计算点
        :param plant_id: 电厂Id
        :param desc: 描述
        :param formula: 公式
        :return: True or False
        """
        json, ok = self.http.trans_post(plant_id, ['powerMobileApp', 'config', 'point', 'defines'],
                                        data={'sisId': None, 'plantId': plant_id,
                                              'description': desc, 'valid': True,
                                              'type': 1, 'formula': formula})
        return json.get(str(plant_id), False) if ok else False

    def get_point(self, plant_id, point_id):
        """
        获取指定定义点
        :param plant_id: 电厂id
        :param point_id: 点Id
        :return: {'id': , 'sisId': , 'description': , 'plantId': , 'type': , 'formula': , 'valid': }
        """
        json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'config', 'point', 'defines', point_id])
        return json.get(str(plant_id)) if ok else None

    def update_point(self, plant_id, point_id, desc, formula):
        """
        更新指定定义点
        :param plant_id: 电厂Id
        :param point_id: 点Id
        :param desc: 描述
        :param formula: 公式
        :return: True or False
        """
        json, ok = self.http.trans_put(plant_id, ['powerMobileApp', 'config', 'point', 'defines'],
                                       data={'id': point_id, 'description': desc, 'formula': formula})
        return json.get(str(plant_id), False) if ok else False

    def get_sampling(self, plant_id, point_id):
        """
        获取指定点的采样信息
        :param plant_id: 电厂Id
        :param point_id: 点Id
        :return: {'id': , 'table': , 'column': }
        """
        json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'config', 'sampling', point_id])
        return json.get(str(plant_id)) if ok else None

    def insert_sampling(self, plant_id, point_id):
        """
        对指定点定义采样
        :param plant_id: 电厂Id
        :param point_id: 点Id
        :return: True or False
        """
        json, ok = self.http.trans_post(plant_id, ['powerMobileApp', 'config', 'sampling', point_id])
        return json.get(str(plant_id), False) if ok else False

    def delete_sampling(self, plant_id, point_id, clear=False):
        """
        删除点采样定义
        :param plant_id: 电厂Id
        :param point_id: 点Id
        :param clear: 是否清除数据
        :return: True or False
        """
        params = {'clear': True} if clear else None
        json, ok = self.http.trans_delete(plant_id, ['powerMobileApp', 'config', 'sampling', point_id],
                                          params=params)
        return json.get(str(plant_id), False) if ok else False

    def get_mapping(self, plant_id, unique_id):
        """
        获取数据分类映射信息
        :param plant_id: 电厂Id
        :param unique_id: 唯一Id
        :return:{'id': , 'desc': , 'pointId': , 'precision': , 'unit': , 'limitUp': , 'limitDown': }
        """
        json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'config', 'mappings', unique_id])
        return json.get(str(plant_id)) if ok else None

    def insert_mapping(self, plant_id, unique_id, desc, point_id, precision, unit, limit_up, limit_down):
        """
        增加数据分类映射信息
        :param plant_id: 电厂Id
        :param unique_id: 唯一Id
        :param desc: 描述
        :param point_id: 点Id
        :param precision: 精度
        :param unit: 单位
        :param limit_up: 上限
        :param limit_down: 下限
        :return: True or False
        """
        data = {'id': unique_id, 'desc': desc, 'pointId': point_id, 'precision': precision, 'unit': unit,
                'limitUp': limit_up, 'limitDown': limit_down}
        json, ok = self.http.trans_post(plant_id, ['powerMobileApp', 'config', 'mappings'], data=data)
        return json.get(str(plant_id), False) if ok else False

    def update_mapping(self, plant_id, unique_id, desc, point_id, precision, unit, limit_up, limit_down):
        """
        更新数据分类映射信息
        :param plant_id: 电厂Id
        :param unique_id: 唯一Id
        :param desc: 描述
        :param point_id: 点Id
        :param precision: 精度
        :param unit: 单位
        :param limit_up: 上限
        :param limit_down: 下限
        :return: True or False
        """
        data = {'id': unique_id, 'desc': desc, 'pointId': point_id, 'precision': precision, 'unit': unit,
                'limitUp': limit_up, 'limitDown': limit_down}
        json, ok = self.http.trans_put(plant_id, ['powerMobileApp', 'config', 'mappings'], data=data)
        return json.get(str(plant_id), False) if ok else False

    def delete_mapping(self, plant_id, unique_id):
        """
        删除数据分类映射信息
        :param plant_id: 电厂Id
        :param unique_id: 唯一Id
        :return: True or False
        """
        json, ok = self.http.trans_delete(plant_id, ['powerMobileApp', 'config', 'mappings', unique_id])
        return json.get(str(plant_id), False) if ok else False

    def get_realtime_data(self, plant_id):
        """
        获取电厂实时数据
        :param plant_id: 电厂Id
        :return: {'time': , 'plantId': , 'values': [{'time': , 'value': , 'pointId': }, ...]}
        """
        json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'data', 'runtime', 'all', plant_id])
        return json.get(str(plant_id), []) if ok else []

    def get_his_data(self, unique_id, t1, t2, correct=False):
        """
        获取历史数据
        :param unique_id: 唯一Id
        :param t1: 起始时间
        :param t2: 结束时间
        :param correct: 是否取修正后的数据
        """
        plant_id = int(unique_id.split(',')[0])
        t1 = self.parser.set_date(t1).set_time(t1).datetime
        t2 = self.parser.set_date(t2).set_time(t2).datetime
        if t1 > t2:
            return []
        params = None if correct else {'raw': 'true'}
        json, ok = self.http.trans_get(plant_id,
                                       ['data', unique_id,
                                        t1.strftime('%Y-%m-%d %H:%M'),
                                        t2.strftime('%Y-%m-%d %H:%M')],
                                       proxy=True, params=params, timeout=300)
        return json.get(str(plant_id), {}).get(unique_id) if ok else None

    def get_all_runtime_data(self, plant_id):
        """
        获取实时数据
        :param plant_id: 电厂Id
        """
        json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'data', 'runtime', 'all', plant_id],
                                       proxy=False, timeout=300)

        return json if ok else None

    def get_page_electric(self, plant_id, type, id):
        """
        获取电量页面数据
        :param plant_id: 电厂Id
        :param type: 类型，包含(plant, zones, units)
        :param id: id,包含(zone_id, unit_id)
        :return: 
        """
        if type == 'plant':
            json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'page', 'electric', 'plant'], proxy=False, timeout=300)
        else:
            json, ok = self.http.trans_get(plant_id, ['powerMobileApp', 'page', 'electric', type, id], proxy=False, timeout=300)

        return json if ok else None


if __name__ == '__main__':
    from datetime import datetime, timedelta

    server = Server('publish')
    data = server.get_his_data('6,7,13,you_gfh', datetime.now() - timedelta(hours=1), datetime.now(), False)
    print(data)
    # data = [(datetime.fromtimestamp(int(k)), v) for k, v in data.items()]
