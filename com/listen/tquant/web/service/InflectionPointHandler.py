# coding: utf-8
from datetime import datetime

from tornado.web import RequestHandler
from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils
import simplejson


class InflectionPointHandler(RequestHandler):
    dbService = DbService()

    def post(self):
        # security_code = self.get_argument('security_code')
        security_code = '002466'
        size = self.get_argument('size', 20)
        if security_code is not None:
            result = self.dbService.get_stock_day_kline(security_code, size)
            result = Utils.tuples_to_dicts(result, self.get_list_keys())
            result = {"rows": result}
            result_json = simplejson.dumps(result, default=Utils.json_default)
            print('get_stock_day_kline result: ', result_json)
            self.write(result_json)
        else:
            self.write("no data!!!")

    @staticmethod
    def get_list_keys():
        list_keys = ['the_date',
                     'amount', 'amount_pre', 'amount_chg',
                     'vol', 'vol_pre', 'vol_chg',
                     'open', 'open_low_chg',
                     'high', 'low', 'high_low_chg', 'high_close_chg',
                     'close', 'close_pre', 'close_chg', 'close_open_chg',
                     'price_avg', 'close_price_avg_chg', 'price_avg_chg']
        return list_keys

    def get(self):
        page = self.get_argument('page_name')
        page = 'modules/' + page
        print(page)
        self.render(page)