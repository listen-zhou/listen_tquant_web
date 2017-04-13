# coding: utf-8

import os.path

import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys


from tornado.options import define, options

from com.listen.tquant.web.dbservice.Service import DbService


class CheckStockIsWrothBuyingHandler(tornado.web.RequestHandler):
    dbService = DbService()

    @staticmethod
    def get_security_info(security_code):
        print('get_security_info', security_code)
        sql = "select security_code, security_name " \
              "from tquant_security_info where security_code = {security_code}"
        sql = sql.format(security_code=CheckStockIsWrothBuyingHandler.quotes_surround(security_code))
        tuple_data = CheckStockIsWrothBuyingHandler.dbService.query(sql)
        if tuple_data is not None and len(tuple_data) > 0:
            return tuple_data[0]
        return None

    @staticmethod
    def get_list_data(security_code):
        if security_code is not None and len(security_code) > 0:
            sql = CheckStockIsWrothBuyingHandler.get_query_sql(security_code)
            print(sql)
            try:
                tuple_data = CheckStockIsWrothBuyingHandler.dbService.query(sql)
                list_data = []
                for item in tuple_data:
                    item_list = CheckStockIsWrothBuyingHandler.analysis_item(item)
                    list_data.append(item_list)
                return list_data
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(exc_type, exc_value, exc_traceback)
            return None
        else:
            return None

    def post(self):
        # method_log_list = self.deepcopy_list(self.log_list)
        security_code = ''
        try:
            security_code = self.get_argument('security_code')
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback)

        security_info = CheckStockIsWrothBuyingHandler.get_security_info(security_code)
        list_data = CheckStockIsWrothBuyingHandler.get_list_data(security_code)
        if list_data is not None and len(list_data) > 0:
                self.render('modules/average_list.html', table=list_data, update_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), security_info=security_info)
        else:
            self.write('没有数据')

    @staticmethod
    def analysis_item(item):
        item_list = []
        i = 0
        while i < len(item):
            if i == 0:
                item_list.append([item[i].strftime('%m%d'), ''])
            elif (i >= 5 and i <= 7) or i == 10 or i == 12 or i == 14 or i == 16 or i == 18 or i == 19:
                item_list.append([item[i], CheckStockIsWrothBuyingHandler.get_css(item[i])])
            else:
                item_list.append([item[i], ''])
            i += 1

        return item_list

    # def get_flow_css(self, val):
    #     if val is None :
    #         return ''
    #     elif val >= 3:
    #         return 'm3'
    #     elif val >= 2:
    #         return 'm2'
    #     elif val >= 1.5:
    #         return 'm1'
    #     elif val > 1:
    #         return 'm0'
    #     elif val < 1:
    #         return 'l0'
    #     elif val <= 0.75:
    #         return 'l1'
    #     elif val <= 0.5:
    #         return 'l2'
    #     elif val <= 0.25:
    #         return 'l3'
    #     else:
    #         return ''

    @staticmethod
    def get_css(val):
        if val is None:
            return ''
        elif val >= 3:
            return 'm3'
        elif val >= 2:
            return 'm2'
        elif val >= 1:
            return 'm1'
        elif val > 0:
            return 'm0'
        elif val <= -3:
            return 'l3'
        elif val <= -2:
            return 'l2'
        elif val <= -1:
            return 'l1'
        elif val < 0:
            return 'l0'
        else:
            return ''

    @staticmethod
    def get_query_sql(security_code):
        sql = "select " \
              "kline.the_date, kline.open, kline.high, kline.low, kline.close, " \
              "kline.close_chg, kline.close_price_avg_chg, ma10close_ma_price_avg_chg, " \
              "kline.vol, kline.amount, ma10amount_flow_chg, kline.price_avg, kline.price_avg_chg, " \
              "ma3_price_avg, ma3_price_avg_chg, " \
              "ma5_price_avg, ma5_price_avg_chg, " \
              "ma10_price_avg, ma10_price_avg_chg, " \
              "ma10_price_avg_chg_avg " \
              "from " \
              "tquant_stock_day_kline kline " \
              "left join " \
              "( select security_code, the_date, price_avg ma3_price_avg, price_avg_chg ma3_price_avg_chg " \
              "from tquant_stock_average_line " \
              "where ma = 3 and security_code = {security_code}) ma3 " \
              "on kline.security_code = ma3.security_code and kline.the_date = ma3.the_date " \
              "left join " \
              "(select security_code, the_date, price_avg ma5_price_avg, price_avg_chg ma5_price_avg_chg " \
              "from tquant_stock_average_line " \
              "where ma = 5 and security_code = {security_code}) ma5 " \
              "on kline.security_code = ma5.security_code and kline.the_date = ma5.the_date " \
              "left join " \
              "(select security_code, the_date, price_avg ma10_price_avg, price_avg_chg ma10_price_avg_chg, " \
              "price_avg_chg_avg ma10_price_avg_chg_avg, close_ma_price_avg_chg ma10close_ma_price_avg_chg, " \
              "amount_flow_chg ma10amount_flow_chg " \
              "from tquant_stock_average_line " \
              "where ma = 10 and security_code = {security_code}) ma10 " \
              "on kline.security_code = ma10.security_code and kline.the_date = ma10.the_date " \
              "where kline.security_code = {security_code} " \
              "order by kline.the_date desc limit 50 "
        sql = sql.format(security_code=CheckStockIsWrothBuyingHandler.quotes_surround(security_code))
        return sql

    @staticmethod
    def quotes_surround(str):
        if str is not None:
            return "'" + str + "'"
        return str
