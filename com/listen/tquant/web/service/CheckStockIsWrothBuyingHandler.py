# coding: utf-8
import calendar
import os.path

import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys


from tornado.options import define, options

from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils


class CheckStockIsWrothBuyingHandler(tornado.web.RequestHandler):

    dbService = DbService()

    def put(self):
        security_code = self.get_argument('security_code')
        worth_value = self.get_argument('worth_value')
        return_dict= {}
        if security_code is None or len(security_code) == 0:
            return_dict['state'] = False
            return_dict['msg'] = '股票代码不能为空'
        else:
            sql = "select count(*) from tquant_security_info where security_code = {security_code}"
            sql = sql.format(security_code=self.quotes_surround(security_code))
            count = self.dbService.query(sql)[0][0]
            if count == 1:
                sql = "update tquant_security_info set worth_buying = {worth_value} where security_code = {security_code}"
                sql = sql.format(security_code=self.quotes_surround(security_code),
                                 worth_value=worth_value)
                self.dbService.update(sql)
                return_dict['state'] = True
                return_dict['msg'] = '操作成功'
            else:
                return_dict['state'] = False
                return_dict['msg'] = '请确认股票代码是否正确'
        self.write(return_dict)

    def get(self):
        list_data = self.dbService.get_stock_worth_buying()
        self.render('modules/worth_buying.html', table=list_data)

    def get_list_data(self, security_code, limit):
        if security_code is not None and len(security_code) > 0:
            sql = self.get_query_sql(security_code, limit)
            print(sql)
            try:
                tuple_data = self.dbService.query(sql)
                list_data = []
                for item in tuple_data:
                    item_list = self.analysis_item(item)
                    list_data.append(item_list)
                return list_data
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(exc_type, exc_value, exc_traceback)
            return None
        else:
            return None



    def post(self):
        security_code = ''
        limit = 50
        try:
            security_code = self.get_argument('security_code')
            limit = self.get_argument('limit')
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback)
        list_data = self.get_list_data(security_code, limit)
        if list_data is not None and len(list_data) > 0:
                self.render('modules/average_list.html', table=list_data)
        else:
            self.write('没有数据')

    def analysis_item(self, item):
        item_list = []
        i = 0
        while i < len(item):
            value = item[i]
            if value is None:
                value = ''
            if i == 0:
                item_list.append([value.strftime('%m%d'), ''])
            elif (i >= 5 and i <= 7) or i == 12 \
                    or i == 14 or i == 16 or i == 18 or i == 19 \
                    or (i >= 24 and i <= 25):
                item_list.append([str(value) + '%', self.get_css(value)])
            elif i >= 21 and i <= 23:
                item_list.append([self.get_diff_arrow(value), ''])
            elif i == 10:
                item_list.append([str(value) + '%', self.get_amount_flow_css(item[12])])
            elif i == 26:
                item_list.append([self.get_amount_flow_arrow(value, item[12]), ''])
            elif i == 27:
                item_list.append([self.get_week_day_num(value), ''])
            elif i == 8:
                item_list.append([Utils.base_round(Utils.division(value, 100), 2), ''])
            elif i == 9:
                item_list.append([Utils.base_round(Utils.division(value, 10000), 2), ''])
            else:
                item_list.append([value, ''])
            i += 1

        return item_list

    def get_week_day_num(self, the_date):
        if the_date is not None:
            year = the_date.year
            month = the_date.month
            day = the_date.day
            return calendar.weekday(year, month, day) + 1

    def get_amount_flow_css(self, price_avg_chg):
        if price_avg_chg is not None:
            if price_avg_chg >= 0:
                return 'm0'
            else:
                return 'l0'
        else:
            return ''

    def get_amount_flow_arrow(self, val, price_avg_chg):
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


    def get_diff_arrow(self, val):
        if val is None or val == '':
            return ''
        if val > 0:
            return '../static/img/up2.gif'
        elif val < 0:
            return '../static/img/down2.gif'
        else:
            return '../static/img/stop2.gif'

    def get_css(self, val):
        if val is None or val == '':
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

    def get_query_sql(self, security_code, limit=50):
        sql = "select " \
              "kline.the_date, kline.open, kline.high, kline.low, kline.close, " \
              "kline.close_chg, kline.close_price_avg_chg, ma10close_ma_price_avg_chg, " \
              "kline.vol, kline.amount, ma10amount_flow_chg, kline.price_avg, kline.price_avg_chg, " \
              "ma3_price_avg, ma3_price_avg_chg, " \
              "ma5_price_avg, ma5_price_avg_chg, " \
              "ma10_price_avg, ma10_price_avg_chg, " \
              "ma10_price_avg_chg_avg, " \
              "0, " \
              "ma3_price_avg_chg_avg_diff, ma5_price_avg_chg_avg_diff, ma10_price_avg_chg_avg_diff," \
              "ma3_price_avg_chg_avg, ma5_price_avg_chg_avg, ma10amount_flow_chg, kline.the_date week_day " \
              "from " \
              "tquant_stock_day_kline kline " \
              "left join " \
              "( select security_code, the_date, price_avg ma3_price_avg, price_avg_chg ma3_price_avg_chg, " \
              "price_avg_chg_avg_diff ma3_price_avg_chg_avg_diff, price_avg_chg_avg ma3_price_avg_chg_avg " \
              "from tquant_stock_average_line " \
              "where ma = 3 and security_code = {security_code}) ma3 " \
              "on kline.security_code = ma3.security_code and kline.the_date = ma3.the_date " \
              "left join " \
              "(select security_code, the_date, price_avg ma5_price_avg, price_avg_chg ma5_price_avg_chg, " \
              "price_avg_chg_avg_diff ma5_price_avg_chg_avg_diff, price_avg_chg_avg ma5_price_avg_chg_avg " \
              "from tquant_stock_average_line " \
              "where ma = 5 and security_code = {security_code}) ma5 " \
              "on kline.security_code = ma5.security_code and kline.the_date = ma5.the_date " \
              "left join " \
              "(select security_code, the_date, price_avg ma10_price_avg, price_avg_chg ma10_price_avg_chg, " \
              "price_avg_chg_avg ma10_price_avg_chg_avg, close_ma_price_avg_chg ma10close_ma_price_avg_chg, " \
              "amount_flow_chg ma10amount_flow_chg, price_avg_chg_avg_diff ma10_price_avg_chg_avg_diff " \
              "from tquant_stock_average_line " \
              "where ma = 10 and security_code = {security_code}) ma10 " \
              "on kline.security_code = ma10.security_code and kline.the_date = ma10.the_date " \
              "where kline.security_code = {security_code} " \
              "order by kline.the_date desc limit {limit} "
        sql = sql.format(security_code=self.quotes_surround(security_code),
                         limit=limit)
        return sql

    def quotes_surround(self, str):
        if str is not None:
            return "'" + str + "'"
        return str
