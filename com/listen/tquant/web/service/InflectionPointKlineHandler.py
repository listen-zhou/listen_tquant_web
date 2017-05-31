# coding: utf-8
from datetime import datetime

from tornado.web import RequestHandler
from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils
import time
import simplejson
from tornado.escape import json_encode, json_decode

class InflectionPointKlineHandler(RequestHandler):
    dbService = DbService()

    def get(self):
        security_code = self.get_argument('security_code', None)
        size = self.get_argument('size', 20)
        if security_code is not None:
            result = self.get_stock_day_kline(security_code, size)
            result = self.get_stock_list_list(result)
            result_json = simplejson.dumps(result)
            print('get_stock_history_kline result: ', result_json)
            self.write(result_json)
        else:
            self.write("no data!!!")

    @staticmethod
    def get_stock_list_list(tuple_datas):
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
        if tuple_datas is not None and len(tuple_datas) > 0:
            result = []
            for i in range(len(tuple_datas)):
                result.append([Utils.format_yyyy_mm_dd(tuple_datas[i][0]),
                               tuple_datas[i][3], tuple_datas[i][6], tuple_datas[i][5], tuple_datas[i][4],
                               tuple_datas[i][2]]
                              )
            return result
        return None

    @staticmethod
    def date2timestamp(date):
        if date is not None:
            date = datetime(date.year, date.month, date.day, 0, 0, 0)
            timestamp = time.mktime(date.timetuple())
            return timestamp * 1000
        return 0


    def get_all_stock_info(self):
        sql = "select security_code, security_name " \
              "from tquant_security_info " \
              "where worth_buying = 1 " \
              "order by security_code asc "
        result = self.dbService.query(sql)
        return result

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
                  "order by the_date asc "
            result = self.dbService.query(sql.format(security_code=Utils.quotes_surround(security_code)))
            return result
        return None