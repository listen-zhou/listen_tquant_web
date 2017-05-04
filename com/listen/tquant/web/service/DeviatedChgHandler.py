# coding: utf-8
from datetime import datetime

from tornado.web import RequestHandler
from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils

class DeviatedChgHandler(RequestHandler):
    dbService = DbService()

    def get_max_the_date(self):
        sql = "select max(the_date) from tquant_stock_day_kline "
        the_date = self.dbService.query(sql)
        if the_date is not None and len(the_date) > 0:
            return the_date[0][0]
        return None

    def get(self):
        max_the_date = self.get_max_the_date()
        if max_the_date is None:
            self.write("a ou, no data.")
        else:
            sql = "select a.security_code, a.the_date, " \
                  "a.amount, a.amount_chg, " \
                  "a.vol, a.vol_chg, " \
                  "a.price_avg, a.close_price_avg_chg, a.price_avg_chg, " \
                  "a.high, a.high_low_chg, a.high_close_chg, " \
                  "a.open, a.open_low_chg, " \
                  "a.close, a.close_chg, a.close_open_chg, " \
                  "a.low, b.security_name " \
                  "from tquant_stock_day_kline a " \
                  "inner join tquant_security_info b " \
                  "on a.security_code = b.security_code " \
                  "where a.the_date = {the_date} " \
                  "and a.close > a.open " \
                  "order by " \
                  "a.high_low_chg desc, " \
                  "a.close_open_chg desc, " \
                  "a.high_close_chg asc, " \
                  "a.open_low_chg asc "
            print('max_the_date', max_the_date)
            result = self.dbService.query(sql.format(the_date=Utils.quotes_surround(max_the_date.strftime('%Y-%m-%d'))))
            if result is not None and len(result) > 0:
                result = self.analysis_data(result)
                self.render('modules/deviated_chg_list.html', table=result)

    def analysis_data(self, result):
        data = []
        if result is not None and len(result) > 0:
            for item in result:
                item_list = []
                i = 0
                while i < len(item):
                    if i == 1:
                        item_list.append([item[i].strftime('%Y-%m-%d'), ''])
                    elif i == 2:
                        item_list.append([Utils.base_round(Utils.division(item[i], 10000), 2), ''])
                    elif i == 4:
                        item_list.append([Utils.base_round(Utils.division(item[i], 100), 2), ''])
                    else:
                        item_list.append([item[i], ''])
                    i += 1
                data.append(item_list)
        return data