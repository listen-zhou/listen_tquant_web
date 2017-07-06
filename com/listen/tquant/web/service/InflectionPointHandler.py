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
        size = self.get_argument('size', 250)
        if security_code is not None:
            result = self.get_stock_day_kline(security_code, size)
            result = Utils.tuples_to_dicts(result, Utils.get_day_kline_list_keys())
            print('result', result)
            if result is None or len(result) == 0:
                self.write('[]')
            else:
                result = {"rows": result}
                result_json = simplejson.dumps(result, default=Utils.json_default)
                print('get_stock_day_kline result: ', result_json)
                self.write(result_json)
        else:
            self.write('[]')

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
        result = Utils.tuples_to_dicts(result, InflectionPointHandler.get_stock_info_list_keys())
        result = {'rows': result}
        result_json = simplejson.dumps(result, default=Utils.json_default)
        print('get_all_stock_info result: ', result_json)
        self.write(result_json)

    @staticmethod
    def get_stock_day_kline_sql(security_code, size=20):
        if security_code is not None:
            sql = "select "
            for field_name in Utils.get_day_kline_list_keys():
                sql += " " + field_name + ","
            sql = sql[0:len(sql) - 1]
            sql += " from tquant_stock_history_quotation " \
                  "where security_code = {security_code} " \
                  "order by the_date desc " \
                  "limit {size}"
            sql = sql.format(security_code=Utils.quotes_surround(security_code), size=size)
            return sql
        else:
            return None

    def get_stock_day_kline(self, security_code, size=20):
        sql = InflectionPointHandler.get_stock_day_kline_sql(security_code, size)
        print(sql)
        if sql is not None:
            result = self.dbService.query(sql)
            return result
        else:
            return None
