# coding: utf-8
from datetime import datetime

from tornado.web import RequestHandler
from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils
import simplejson


class InflectionPointHandler(RequestHandler):
    dbService = DbService()

    def post(self):
        security_code = self.get_argument('security_code', None)
        size = self.get_argument('size', 100)
        if security_code is not None:
            result = self.get_stock_day_kline(security_code, size)
            result = Utils.tuples_to_dicts(result, self.get_day_kline_list_keys())
            print('result', result)
            result = Utils.append_week_day(result)
            result = {"rows": result}
            result_json = simplejson.dumps(result, default=Utils.json_default)
            print('get_stock_day_kline result: ', result_json)
            self.write(result_json)
        else:
            self.write("no data!!!")

    @staticmethod
    def get_day_kline_list_keys():
        list_keys = ['the_date',
                     'amount',
                     'vol', 'open', 'high', 'low', 'close',
                     'vol_chg', 'close_chg', 'close_open_chg',
                     'price_avg', 'price_avg_chg', 'close_price_avg_chg',
                     'price_avg_3', 'price_avg_chg_3',
                     'price_avg_5', 'price_avg_chg_5',
                     'price_avg_10', 'price_avg_chg_10', 'close_10_price_avg_chg',
                     'price_avg_chg_10_avg', 'price_avg_chg_10_avg_diff', 'money_flow'
                     ]
        return list_keys

    @staticmethod
    def get_amount_flow_arrow(val, price_avg_chg):
        if val is not None and price_avg_chg is not None:
            if price_avg_chg > 0:
                if val > 100 and val < 150:
                    return '../static/img/stop2.gif'
                elif val >= 150 and val < 200:
                    return '../static/img/up2.gif'
                elif val >= 200:
                    return '../static/img/up1.gif'
                elif val == 100:
                    return ''
                elif val < 70 and val > 50:
                    return '../static/img/down4.gif'
                elif val <= 50 and val > 0:
                    return '../static/img/down3.gif'
                else:
                    return ''
            elif price_avg_chg < 0:
                if val > 100 and val < 150:
                    return '../static/img/stop3.gif'
                elif val >= 150 and val < 200:
                    return '../static/img/up4.gif'
                elif val >= 200:
                    return '../static/img/up3.gif'
                elif val == 100:
                    return ''
                elif val < 70 and val > 50:
                    return '../static/img/down2.gif'
                elif val <= 50 and val > 0:
                    return '../static/img/down1.gif'
                else:
                    return ''
            else:
                return ''

    @staticmethod
    def get_diff_up_down_img(val):
        if val is None or val == '':
            return ''
        if val >= 1:
            return '../static/img/up1.gif'
        elif val > 0:
            return '../static/img/up2.gif'
        elif val == 0:
            return '../static/img/stop2.gif'
        elif val <= -1:
            return '../static/img/down1.gif'
        elif val < 0:
            return '../static/img/down2.gif'


    def get_all_stock_info(self):
        sql = "select security_code, security_name " \
              "from tquant_security_info " \
              "where worth_buying = 1 " \
              "order by security_code asc "
        result = self.dbService.query(sql)
        return result

    @staticmethod
    def get_stock_info_list_keys():
        list_keys = ['security_code', 'security_name']
        return list_keys

    def get(self):
        result = self.get_all_stock_info()
        result = Utils.tuples_to_dicts(result, self.get_stock_info_list_keys())
        result = {'rows': result}
        result_json = simplejson.dumps(result, default=Utils.json_default)
        print('get_all_stock_info result: ', result_json)
        self.write(result_json)

    def get_stock_day_kline(self, security_code, size=20):
        if security_code is not None:
            """
            'the_date',
                     'amount',
                     'vol', 'open', 'high', 'low', 'close',
                     'vol_chg', 'close_chg', 'close_open_chg',
                     'price_avg', 'price_avg_chg', 'close_price_avg_chg',
                     'price_avg_3', 'price_avg_chg_3',
                     'price_avg_5', 'price_avg_chg_5',
                     'price_avg_10', 'price_avg_chg_10', 'close_10_price_avg_chg',
                     'price_avg_chg_10_avg', 'price_avg_chg_10_avg_diff', 'money_flow'
            """
            sql = "select " \
                  "the_date, " \
                  "amount, " \
                  "vol, open, high, low, close, " \
                  "vol_chg, close_chg, close_open_chg, " \
                  "price_avg, price_avg_chg, close_price_avg_chg, " \
                  "price_avg_3, price_avg_chg_3, " \
                  "price_avg_5, price_avg_chg_5, " \
                  "price_avg_10, price_avg_chg_10, close_10_price_avg_chg, " \
                  "price_avg_chg_10_avg, price_avg_chg_10_avg_diff, money_flow " \
                  "from tquant_stock_history_quotation " \
                  "where security_code = {security_code} " \
                  "order by the_date desc " \
                  "limit {size}"
            result = self.dbService.query(sql.format(security_code=Utils.quotes_surround(security_code), size=size))
            return result
        return None