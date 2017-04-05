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
                print(tuple_data)
                list_data = []
                for item in tuple_data:
                    item_dict = {
                        'the_date': item[0].strftime('%Y-%m-%d'),
                        'close': item[1], 'amount': item[2], 'vol': item[3],

                        'ma3_close_avg': item[4], 'ma3_close_avg_chg': item[5], 'ma3_close_avg_chg_avg': item[6],
                        'ma3_amount_avg': item[7], 'ma3_amount_avg_chg': item[8], 'ma3_amount_avg_chg_avg': item[9],
                        'ma3_vol_avg': item[10], 'ma3_vol_avg_chg': item[11], 'ma3_vol_avg_chg_avg': item[12],
                        'ma3_price_avg': item[13], 'ma3_price_avg_chg': item[14], 'ma3_price_avg_chg_avg': item[15],
                        'ma3_amount_flow_chg': item[16], 'ma3_amount_flow_chg_avg': item[17],
                        'ma3_vol_flow_chg': item[18], 'ma3_vol_flow_chg_avg': item[19],

                        'ma5_close_avg': item[20], 'ma5_close_avg_chg': item[21], 'ma5_close_avg_chg_avg': item[22],
                        'ma5_amount_avg': item[23], 'ma5_amount_avg_chg': item[24], 'ma5_amount_avg_chg_avg': item[25],
                        'ma5_vol_avg': item[26], 'ma5_vol_avg_chg': item[27], 'ma5_vol_avg_chg_avg': item[28],
                        'ma5_price_avg': item[29], 'ma5_price_avg_chg': item[30], 'ma5_price_avg_chg_avg': item[31],
                        'ma5_amount_flow_chg': item[32], 'ma5_amount_flow_chg_avg': item[33],
                        'ma5_vol_flow_chg': item[34], 'ma5_vol_flow_chg_avg': item[35],

                        'ma10_close_avg': item[36], 'ma10_close_avg_chg': item[37], 'ma10_close_avg_chg_avg': item[38],
                        'ma10_amount_avg': item[39], 'ma10_amount_avg_chg': item[40], 'ma10_amount_avg_chg_avg': item[41],
                        'ma10_vol_avg': item[42], 'ma10_vol_avg_chg': item[43], 'ma10_vol_avg_chg_avg': item[44],
                        'ma10_price_avg': item[45], 'ma10_price_avg_chg': item[46], 'ma10_price_avg_chg_avg': item[47],
                        'ma10_amount_flow_chg': item[48], 'ma10_amount_flow_chg_avg': item[49],
                        'ma10_vol_flow_chg': item[50], 'ma10_vol_flow_chg_avg': item[51],

                    }
                    list_data.append(item_dict)
                print(list_data)
                for table in list_data:
                    result = self.render_string('modules/average.html', table=table).decode('utf-8')
                    self.write(result)
                self.finish()
            except Exception:
                sys.exc_info()
        else:
            self.write('aa')

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
