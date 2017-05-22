# coding: utf-8
from datetime import datetime

from tornado.web import RequestHandler
from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils
import simplejson


class InflectionPointHandler(RequestHandler):
    dbService = DbService()

    def post(self):
        security_code = self.get_argument('security_code')
        size = self.get_argument('size', 20)
        if security_code is not None:
            result = self.get_stock_day_kline(security_code, size)
            result = Utils.tuples_to_dicts(result, self.get_day_kline_list_keys())
            result = {"rows": result}
            result_json = simplejson.dumps(result, default=Utils.json_default)
            print('get_stock_day_kline result: ', result_json)
            self.write(result_json)
        else:
            self.write("no data!!!")

    @staticmethod
    def get_day_kline_list_keys():
        list_keys = ['the_date',
                     'amount', 'amount_pre', 'amount_chg',
                     'vol', 'vol_pre', 'vol_chg',
                     'open', 'open_low_chg',
                     'high', 'low', 'high_low_chg', 'high_close_chg',
                     'close', 'close_pre', 'close_chg', 'close_open_chg',
                     'price_avg', 'close_price_avg_chg', 'price_avg_chg']
        return list_keys

    def get_all_stock_info(self):
        sql = "select security_code, security_name from tquant_security_info order by security_code asc "
        result = self.dbService.query(sql)
        return result

    @staticmethod
    def get_stock_info_list_keys():
        list_keys = ['security_code', 'security_name']
        return list_keys

    def get(self):
        result = self.get_all_stock_info()
        result = Utils.tuples_to_dicts(result, self.get_stock_info_list_keys())
        result = {'row': result}
        result_json = simplejson.dumps(result, default=Utils.json_default)
        print('get_all_stock_info result: ', result_json)
        self.write(result_json)

    def get_stock_day_kline(self, security_code, size=20):
        if security_code is not None:
            """
            `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
            `security_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
            `the_date` DATE NOT NULL COMMENT '交易日',
            `amount` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '交易额(元)',
            `amount_pre` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '前一日交易额(元)',
            `amount_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '交易额涨跌幅',
            `vol` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '交易量(手)',
            `vol_pre` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '前一日交易量(手)',
            `vol_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '交易量涨跌幅',
            `open` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '开盘价',
            `open_low_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '开盘价与最低价偏离幅度',
            `high` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '最高价',
            `low` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '最低价',
            `high_low_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '最高价与最低价偏离幅度',
            `high_close_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '最高价与收盘价偏离幅度',
            `close` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '收盘价',
            `close_pre` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '前一日收盘价',
            `close_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '收盘价涨跌幅',
            `close_open_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '收盘价与开盘价偏离幅度',
            `price_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '日均价',
            `close_price_avg_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '收盘/日均价百分比',
            `price_avg_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '日均价涨跌幅百分比',
                    """
            sql = "select " \
                  "the_date, " \
                  "amount, amount_pre, amount_chg, " \
                  "vol, vol_pre, vol_chg, " \
                  "open, open_low_chg, " \
                  "high, low, high_low_chg, high_close_chg, " \
                  "close, close_pre, close_chg, close_open_chg, " \
                  "price_avg, close_price_avg_chg, price_avg_chg " \
                  "from tquant_stock_day_kline " \
                  "where security_code = {security_code} " \
                  "order by the_date desc " \
                  "limit {size}"
            result = self.dbService.query(sql.format(security_code=Utils.quotes_surround(security_code), size=size))
            return result
        return None