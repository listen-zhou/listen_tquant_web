# coding: utf-8

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys


from tornado.options import define, options

from com.listen.tquant.web.dbservice.Service import DbService


class CheckStockIsWrothBuyingHandler(tornado.web.RequestHandler):

    def post(self):
        dbService = DbService()
        # method_log_list = self.deepcopy_list(self.log_list)
        security_code = ''
        start_date = ''
        end_date = ''
        try:
            security_code = self.get_argument('security_code')
            start_date = self.get_argument('start_date')
            end_date = self.get_argument('end_date')
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback)

        if start_date is None or len(start_date) == 0:
            sql = "select the_date from tquant_calendar_info order by the_date desc limit 20 "
            tuple_the_date = dbService.query(sql)
            if tuple_the_date is not None and len(tuple_the_date) > 0:
                start_date = tuple_the_date[len(tuple_the_date) - 1][0].strftime('%Y-%m-%d')
                end_date = tuple_the_date[0][0].strftime('%Y-%m-%d')

        if security_code is not None and len(security_code) > 0:
            sql = self.get_query_sql(security_code, start_date, end_date)
            try:
                tuple_data = dbService.query(sql)
                for item in tuple_data:
                    item_list = self.analysis_item(item)
                    result = self.render_string('modules/average.html', table=item_list).decode('utf-8')
                    self.write(result)
                self.finish()
            except Exception:
                sys.exc_info()
        else:
            self.write('没有数据')

    def analysis_item(self, item):
        item_list = [
            [item[0].strftime('%Y-%m-%d'), ''],
            [item[1], ''],
            [item[2], ''],
            [item[3], ''],

            [item[4], ''],
            [item[5], self.get_css(item[5])],
            [item[6], self.get_css(item[6])],

            [item[7], ''],
            [item[8], self.get_css(item[8])],
            [item[9], self.get_css(item[9])],

            [item[10], ''],
            [item[11], self.get_css(item[11])],
            [item[12], self.get_css(item[12])],

            [item[13], ''],
            [item[14], self.get_css(item[14])],
            [item[15], self.get_css(item[15])],

            [item[16], self.get_css(item[16])],
            [item[17], self.get_css(item[17])],

            [item[18], self.get_css(item[18])],
            [item[19], self.get_css(item[19])],

            [item[20], ''],
            [item[21], self.get_css(item[21])],
            [item[22], self.get_css(item[22])],

            [item[23], ''],
            [item[24], self.get_css(item[24])],
            [item[25], self.get_css(item[25])],

            [item[26], ''],
            [item[27], self.get_css(item[27])],
            [item[28], self.get_css(item[28])],

            [item[29], ''],
            [item[30], self.get_css(item[30])],
            [item[31], self.get_css(item[31])],

            [item[32], self.get_css(item[32])],
            [item[33], self.get_css(item[33])],

            [item[34], self.get_css(item[34])],
            [item[35], self.get_css(item[35])],

            [item[36], ''],
            [item[37], self.get_css(item[37])],
            [item[38], self.get_css(item[38])],

            [item[39], ''],
            [item[40], self.get_css(item[40])],
            [item[41], self.get_css(item[41])],

            [item[42], ''],
            [item[43], self.get_css(item[43])],
            [item[44], self.get_css(item[44])],

            [item[45], ''],
            [item[46], self.get_css(item[46])],
            [item[47], self.get_css(item[47])],

            [item[48], self.get_css(item[48])],
            [item[49], self.get_css(item[49])],

            [item[50], self.get_css(item[50])],
            [item[51], self.get_css(item[51])],
        ]
        return item_list

    def get_css(self, val):
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

    def get_query_sql(self, security_code, start_date, end_date):
        sql = "select ma3.the_date, ma3.close, ma3.amount, ma3.vol, " \
              "ma3.close_avg ma3_close_avg, ma3.close_avg_chg ma3_close_avg_chg, ma3.close_avg_chg_avg ma3_close_avg_chg_avg, " \
              "ma3.amount_avg ma3_amount_avg, ma3.amount_avg_chg ma3_amount_avg_chg, ma3.amount_avg_chg_avg ma3_amount_avg_chg_avg, " \
              "ma3.vol_avg ma3_vol_avg, ma3.vol_avg_chg ma3_vol_avg_chg, ma3.vol_avg_chg_avg ma3_vol_avg_chg_avg, " \
              "ma3.price_avg ma3_price_avg, ma3.price_avg_chg ma3_price_avg_chg, ma3.price_avg_chg_avg ma3_price_avg_chg_avg, " \
              "ma3.amount_flow_chg ma3_amount_flow_chg, ma3.amount_flow_chg_avg ma3_amount_flow_chg_avg, " \
              "ma3.vol_flow_chg ma3_vol_flow_chg, ma3.vol_flow_chg_avg ma3_vol_flow_chg_avg, " \
              "" \
              "ma5.close_avg ma5_close_avg, ma5.close_avg_chg ma5_close_avg_chg, ma5.close_avg_chg_avg ma5_close_avg_chg_avg, " \
              "ma5.amount_avg ma5_amount_avg, ma5.amount_avg_chg ma5_amount_avg_chg, ma5.amount_avg_chg_avg ma5_amount_avg_chg_avg, " \
              "ma5.vol_avg ma5_vol_avg, ma5.vol_avg_chg ma5_vol_avg_chg, ma5.vol_avg_chg_avg ma5_vol_avg_chg_avg, " \
              "ma5.price_avg ma5_price_avg, ma5.price_avg_chg ma5_price_avg_chg, ma5.price_avg_chg_avg ma5_price_avg_chg_avg, " \
              "ma5.amount_flow_chg ma5_amount_flow_chg, ma5.amount_flow_chg_avg ma5_amount_flow_chg_avg, " \
              "ma5.vol_flow_chg ma5_vol_flow_chg, ma5.vol_flow_chg_avg ma5_vol_flow_chg_avg, " \
              "" \
              "ma10.close_avg ma10_close_avg, ma10.close_avg_chg ma10_close_avg_chg, ma10.close_avg_chg_avg ma10_close_avg_chg_avg, " \
              "ma10.amount_avg ma10_amount_avg, ma10.amount_avg_chg ma10_amount_avg_chg, ma10.amount_avg_chg_avg ma10_amount_avg_chg_avg, " \
              "ma10.vol_avg ma10_vol_avg, ma10.vol_avg_chg ma10_vol_avg_chg, ma10.vol_avg_chg_avg ma10_vol_avg_chg_avg, " \
              "ma10.price_avg ma10_price_avg, ma10.price_avg_chg ma10_price_avg_chg, ma10.price_avg_chg_avg ma10_price_avg_chg_avg, " \
              "ma10.amount_flow_chg ma10_amount_flow_chg, ma10.amount_flow_chg_avg ma10_amount_flow_chg_avg, " \
              "ma10.vol_flow_chg ma10_vol_flow_chg, ma10.vol_flow_chg_avg ma10_vol_flow_chg_avg " \
              "" \
              "from (" \
              "select * from tquant_stock_average_line " \
              "where ma = 3 and security_code = {security_code} and the_date >= {start_date} and the_date <= {end_date}" \
              ") ma3 " \
              "left join " \
              "(select * from tquant_stock_average_line " \
              "where ma = 5 and security_code = {security_code} and the_date >= {start_date} and the_date <= {end_date}" \
              ") ma5 " \
              "on ma3.the_date = ma5.the_date " \
              "left join " \
              "(select * from tquant_stock_average_line " \
              "where ma = 10 and security_code = {security_code} and the_date >= {start_date} and the_date <= {end_date}" \
              ") ma10 on ma3.the_date = ma10.the_date " \
              "order by ma3.the_date desc "
        sql = sql.format(security_code=self.quotes_surround(security_code),
                         start_date=self.quotes_surround(start_date),
                         end_date=self.quotes_surround(end_date)
                         )
        return sql

    def quotes_surround(self, str):
        if str is not None:
            return "'" + str + "'"
        return str
