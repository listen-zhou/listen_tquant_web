# coding: utf-8
from datetime import datetime

from tornado.web import RequestHandler
from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils
import time
import simplejson


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
            # result = [
            #     [1362096000000, 438.00, 438.18, 429.98, 430.47, 19730256],
            #     [1362355200000, 427.80, 428.20, 419.00, 420.05, 20812057],
            #     [1362441600000, 421.48, 435.19, 420.75, 431.14, 22801006],
            #     [1362528000000, 434.51, 435.25, 424.43, 425.66, 16437467],
            #     [1362614400000, 424.50, 432.01, 421.06, 430.58, 16731118],
            #     [1362700800000, 429.80, 435.43, 428.61, 431.72, 13985569],
            #     [1362960000000, 429.75, 439.01, 425.14, 437.87, 16936908],
            #     [1363046400000, 435.60, 438.88, 427.57, 428.43, 16639639],
            #     [1363132800000, 428.45, 434.50, 425.36, 428.35, 14493456],
            #     [1363219200000, 432.83, 434.64, 430.45, 432.50, 10852678],
            #     [1363305600000, 437.93, 444.23, 437.25, 443.66, 22998541],
            #     [1363564800000, 441.45, 457.46, 441.20, 455.72, 21649870],
            #     [1363651200000, 459.50, 460.97, 448.50, 454.49, 18813330],
            #     [1363737600000, 457.42, 457.63, 449.59, 452.08, 11023594],
            #     [1363824000000, 450.22, 457.98, 450.10, 452.73, 13687630],
            #     [1363910400000, 454.58, 462.10, 453.11, 461.91, 14110873],
            #     [1364169600000, 464.69, 469.95, 461.78, 463.58, 17897634],
            #     [1364256000000, 465.44, 465.84, 460.53, 461.14, 10510489],
            #     [1364342400000, 456.46, 456.80, 450.73, 452.08, 11836042],
            #     [1364428800000, 449.82, 451.82, 441.62, 442.66, 15820798],
            # ]
            # result_json = simplejson.dumps(result)
            # print('get_stock_history_kline result: ', result_json)
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
                result.append([InflectionPointKlineHandler.date2timestamp(tuple_datas[i][0]),
                               tuple_datas[i][3], tuple_datas[i][4], tuple_datas[i][5], tuple_datas[i][6],
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
                  "order by the_date desc " \
                  "limit {size}"
            result = self.dbService.query(sql.format(security_code=Utils.quotes_surround(security_code), size=size))
            return result
        return None