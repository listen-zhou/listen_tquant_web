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
                list_data = []
                indexes = [0, 1, 2, 3,
                           13, 14, 15,
                           29, 30, 31,
                           36, 37, 38,
                           39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49
                           ]
                for item in tuple_data:
                    item_list = self.analysis_item(item, indexes)
                    list_data.append(item_list)
                self.render('modules/average_list.html', table=list_data, indexes=indexes, thead_dict=self.get_table_thead_dict())
            except Exception:
                sys.exc_info()
        else:
            self.write('没有数据')

    @staticmethod
    def get_table_thead_dict():
        thead_dict = {}
        thead_dict[0] = '交易日'
        thead_dict[1] = '收'
        thead_dict[2] = '钱'
        thead_dict[3] = '量'

        thead_dict[4] = 'ma3收均'
        thead_dict[5] = 'ma3收均幅'
        thead_dict[6] = 'ma3收均幅均'

        thead_dict[7] = 'ma3日均钱'
        thead_dict[8] = 'ma3日均钱幅'
        thead_dict[9] = 'ma3日均钱幅均'

        thead_dict[10] = 'ma3日均量'
        thead_dict[11] = 'ma3日均量幅'
        thead_dict[12] = 'ma3日均量幅均'

        thead_dict[13] = 'ma3价均'
        thead_dict[14] = 'ma3价均幅'
        thead_dict[15] = 'ma3价均幅均'

        thead_dict[16] = 'ma3钱留幅'
        thead_dict[17] = 'ma3钱留幅均'

        thead_dict[18] = 'ma3量留幅'
        thead_dict[19] = 'ma3量留幅均'

        thead_dict[20] = 'ma5收均'
        thead_dict[21] = 'ma5收均幅'
        thead_dict[22] = 'ma5收均幅均'

        thead_dict[23] = 'ma5日均钱'
        thead_dict[24] = 'ma5日均钱幅'
        thead_dict[25] = 'ma5日均钱幅均'

        thead_dict[26] = 'ma5日均量'
        thead_dict[27] = 'ma5日均量幅'
        thead_dict[28] = 'ma5日均量幅均'

        thead_dict[29] = 'ma5价均'
        thead_dict[30] = 'ma5价均幅'
        thead_dict[31] = 'ma5价均幅均'

        thead_dict[32] = 'ma5钱留幅'
        thead_dict[33] = 'ma5钱留幅均'

        thead_dict[34] = 'ma5量留幅'
        thead_dict[35] = 'ma5量留幅均'

        thead_dict[36] = 'ma10收均'
        thead_dict[37] = 'ma10收均幅'
        thead_dict[38] = 'ma10收均幅均'

        thead_dict[39] = 'ma10日均钱'
        thead_dict[40] = 'ma10日均钱幅'
        thead_dict[41] = 'ma10日均钱幅均'

        thead_dict[42] = 'ma10日均量'
        thead_dict[43] = 'ma10日均量幅'
        thead_dict[44] = 'ma10日均量幅均'

        thead_dict[45] = 'ma10价均'
        thead_dict[46] = 'ma10价均幅'
        thead_dict[47] = 'ma10价均幅均'

        thead_dict[48] = 'ma10钱留幅'
        thead_dict[49] = 'ma10钱留幅均'

        thead_dict[50] = 'ma10量留幅'
        thead_dict[51] = 'ma10量留幅均'

        return thead_dict

    def get_table_thead_fields(self, indexes):
        thead_fields = []
        thead_dice = CheckStockIsWrothBuyingHandler.get_table_thead_dict()
        for i in indexes:
            thead_fields.append(thead_dice[i])
        return thead_fields


    def analysis_item(self, item, indexes):
        item_list = []
        for i in indexes:
            if i == 0:
                item_list.append([item[i].strftime('%m%d'), ''])
            elif i >= 1 and i <= 3:
                item_list.append([item[i], ''])
            elif (i >= 16 and i <= 19) or (i >= 32 and i <= 35) or (i >= 48 and i <= 51):
                item_list.append([item[i], self.get_css(item[i])])
            elif i == 4 or i == 7 or i == 10 or i == 13 \
                    or i == 20 or i == 23 or i == 26 or i == 29 \
                    or i == 36 or i == 39 or i == 42 or i == 45:
                item_list.append([item[i], ''])
            else:
                item_list.append([item[i], self.get_css(item[i])])

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
