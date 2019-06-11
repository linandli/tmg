import logging
from datetime import datetime, timedelta

from lib.server import Server
from lib.singleton import Singleton


class Utils(metaclass=Singleton):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.server = Server('publish', timeout=15)

    def get_fh(self, plant, start_time, end_time):
        start_time = (datetime.now() - timedelta(minutes=60 * 3)
                      ).strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res = dict()
        _fh_info = dict()
        self.logger.info('start get plant_id: %s of fh' % plant)
        units = self.server.get_units(plant)
        for item in units:
            _unit_info = {'name': item['unit_name'], 'code': '%(plant_id)s,%(zone_id)s,%(unit_id)s,you_gfh' % item}
            _zone_info = {'name': item['zone_name'], 'code': '%(plant_id)s,%(zone_id)s,0,you_gfh' % item}
            _plant_info = {'name': item['plant_name'], 'code': '%(plant_id)s,0,0,you_gfh' % item}
            if 'unit' not in _fh_info:
                _fh_info['unit'] = [_unit_info]
            elif _unit_info not in _fh_info['unit']:
                _fh_info['unit'].append(_unit_info)
            if 'zone' not in _fh_info:
                _fh_info['zone'] = [_zone_info]
            elif _zone_info not in _fh_info['zone']:
                _fh_info['zone'].append(_zone_info)
            if 'plant' not in _fh_info:
                _fh_info['plant'] = [_plant_info]        
        for key, info in _fh_info.items():
            if key not in res:
                res[key] = list()
            res[key].append({item['name']: self.server.get_his_data(item['code'], start_time, end_time) for item in info})
        return res
