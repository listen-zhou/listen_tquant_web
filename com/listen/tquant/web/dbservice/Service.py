# -*- coding: utf-8 -*-

import pymysql
import configparser
import os
import traceback
import sys

from decimal import Decimal

from com.listen.tquant.web.utils.Utils import Utils


class DbService(object):
    def __init__(self):
        # charset必须设置为utf8，而不能为utf-8
        config = configparser.ConfigParser()
        os.chdir('../config')
        config.read('database.cfg')
        mysql_section = config['mysql']
        if mysql_section:
            host = mysql_section['db.host']
            port = int(mysql_section['db.port'])
            username = mysql_section['db.username']
            password = mysql_section['db.password']
            dbname = mysql_section['db.dbname']
            charset = mysql_section['db.charset']
            self.conn = pymysql.connect(host=host, port=port, user=username, passwd=password, db=dbname, charset=charset)
            self.conn.autocommit(True)
            self.cursor = self.conn.cursor()
        else:
            raise FileNotFoundError('database.cfg mysql section not found!!!')

    # 数据库连接关闭
    def close(self):
        if self.cursor:
            self.cursor.close()
            print('---> 关闭游标')
        if self.conn:
            self.conn.close()
            print('---> 关闭连接')

    def update(self, sql):
        try:
            if sql:
                count = self.cursor.execute(sql)
                return count
            else:
                return 0
        except Exception:
            print('error sql:', sql)
            traceback.format_exc()

    # noinspection SpellCheckingInspection
    def insert(self, upsert_sql):
        try:
            if upsert_sql:
                self.cursor.execute(upsert_sql)
                return True
            else:
                return False
        except Exception:
            print('error sql:', upsert_sql)
            traceback.format_exc()

    # noinspection SpellCheckingInspection,PyBroadException
    def insert_many(self, upsert_sql_list):
        try:
            if upsert_sql_list:
                for upsert_sql in upsert_sql_list:
                    try:
                        self.cursor.execute(upsert_sql)
                    except Exception:
                        print('error sql:', upsert_sql)
                        self.conn.rollback()
                        traceback.print_exc()
                        return False
                return True
            return False
        except Exception:
            self.conn.rollback()
            traceback.print_exc()

    def query(self, query_sql):
        try:
            if query_sql:
                self.cursor.execute(query_sql)
                stock_tuple_tuple = self.cursor.fetchall()
                return stock_tuple_tuple
            else:
                return None
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback, 'sql error:', query_sql)
            return None

    def query_all_security_codes(self):
        sql = "select security_code, exchange_code " \
              "from tquant_security_info " \
              "where security_type = 'STOCK'"
        return self.query(sql)

    def get_calendar_max_the_date(self):
        """
        查询交易日表中最大交易日日期
        :return:
        """
        sql = "select max(the_date) max_the_date from tquant_calendar_info"
        the_date = self.query(sql)
        if the_date is not None and len(the_date) > 0:
            max_the_date = the_date[0][0]
            return max_the_date
        return None

    def get_batch_list_security_codes(self, batch_size):
        tuple_security_codes = self.query_all_security_codes()
        if tuple_security_codes is not None and len(tuple_security_codes) > 0:
            batch_list = []
            size = len(tuple_security_codes)
            # 分组后余数
            remainder = size % batch_size
            if remainder > 0:
                remainder = 1
            # 分组数，取整数，即批量的倍数
            multiple = size // batch_size
            total = remainder + multiple
            print('size:', size, 'batch:', batch_size, 'remainder:', remainder, 'multiple:', multiple, 'total:', total)
            i = 0
            while i < total:
                # 如果是最后一组，则取全量
                if i == total - 1:
                    temp_tuple = tuple_security_codes[i * batch_size:size]
                else:
                    temp_tuple = tuple_security_codes[i * batch_size:(i + 1) * batch_size]
                batch_list.append(temp_tuple)
                i += 1
            return batch_list
        return None

    def get_batch_list_except_security_codes(self):
        sql = "select c.security_code, c.exchange_code " \
              "from " \
              "( " \
              "select a.security_code, a.exchange_code, a.k_count, b.avg_count ," \
              "b.ma, (a.k_count-b.avg_count + 1) diff " \
              "from " \
              "( " \
              "select security_code, exchange_code, count(*) k_count " \
              "from tquant_stock_day_kline " \
              "group by security_code, exchange_code" \
              ") a " \
              "left join " \
              "( " \
              "select security_code, exchange_code, ma, count(*) avg_count " \
              "from tquant_stock_average_line " \
              "group by security_code, exchange_code, ma" \
              ") b " \
              "on a.security_code = b.security_code and b.exchange_code = a.exchange_code " \
              "having (a.k_count-b.avg_count + 1) != b.ma ) c " \
              "group by c.security_code, c.exchange_code "
        tuple_security_codes = self.query(sql)
        if tuple_security_codes is not None and len(tuple_security_codes) > 0:
            return tuple_security_codes
        return None

    def get_day_kline_except_security_codes(self):
        sql = "select security_code, exchange_code " \
              "from " \
              "( " \
              "select security_code, exchange_code " \
              "from tquant_stock_day_kline " \
              "where close is null or close <= 0 " \
              "or open is null or open <= 0 " \
              "or high <= 0 or high is null " \
              "or low <= 0 or low is null " \
              "group by security_code, exchange_code " \
              ") a"
        tuple_security_codes = self.query(sql)
        if tuple_security_codes is not None and len(tuple_security_codes) > 0:
            return tuple_security_codes
        return None

    def get_stock_worth_buying(self):
        sql = "select security_code, security_name " \
              "from tquant_security_info " \
              "where worth_buying > 0 " \
              "order by security_code asc "
        tuple_data = self.query(sql)
        return tuple_data

    def codes_list_keys(self):
        list_keys = ['security_code', 'security_name']
        return list_keys

    def get_worth_buying_list_dict_codes(self):
        tuples_data = self.get_stock_worth_buying()
        if tuples_data is not None and len(tuples_data) > 0:
            print('get_stock_worth_buying:', tuples_data)
            result = self.tuples_to_list_dict(tuples_data, self.codes_list_keys())
            return result
        else:
            return None

    def worth_buying_list_keys(self):
        list_keys = [
            'the_date',
            'amount',
            'amount_chg',
            'vol',
            'open',
            'open_low_chg',
            'high',
            'low',
            'high_low_chg',
            'high_close_chg',
            'close',
            'close_pre',
            'close_chg',
            'close_open_chg',
            'close_open_chg',
            'price_avg',
            'close_price_avg_chg',
            'price_avg_chg',

            'ma3_close_avg',
            'ma3_close_avg_chg',
            'ma3_close_avg_chg_avg',
            'ma3_close_avg_chg_avg_diff',

            'ma3_amount_avg',
            'ma3_amount_avg_chg',
            'ma3_amount_avg_chg_avg',
            'ma3_amount_avg_chg_avg_diff',

            'ma3_vol_avg',
            'ma3_vol_avg_chg',
            'ma3_vol_avg_chg_avg',
            'ma3_vol_avg_chg_avg_diff',

            'ma3_price_avg',
            'ma3_price_avg_chg',
            'ma3_price_avg_chg_avg',
            'ma3_price_avg_chg_avg_diff',

            'ma3_amount_flow_chg',
            'ma3_amount_flow_chg_avg',
            'ma3_amount_flow_chg_avg_diff',

            'ma3_close_ma_price_avg_chg',

            'ma5_close_avg',
            'ma5_close_avg_chg',
            'ma5_close_avg_chg_avg',
            'ma5_close_avg_chg_avg_diff',

            'ma5_amount_avg',
            'ma5_amount_avg_chg',
            'ma5_amount_avg_chg_avg',
            'ma5_amount_avg_chg_avg_diff',

            'ma5_vol_avg',
            'ma5_vol_avg_chg',
            'ma5_vol_avg_chg_avg',
            'ma5_vol_avg_chg_avg_diff',

            'ma5_price_avg',
            'ma5_price_avg_chg',
            'ma5_price_avg_chg_avg',
            'ma5_price_avg_chg_avg_diff',

            'ma5_amount_flow_chg',
            'ma5_amount_flow_chg_avg',
            'ma5_amount_flow_chg_avg_diff',

            'ma5_close_ma_price_avg_chg',

            'ma10_close_avg',
            'ma10_close_avg_chg',
            'ma10_close_avg_chg_avg',
            'ma10_close_avg_chg_avg_diff',

            'ma10_amount_avg',
            'ma10_amount_avg_chg',
            'ma10_amount_avg_chg_avg',
            'ma10_amount_avg_chg_avg_diff',

            'ma10_vol_avg',
            'ma10_vol_avg_chg',
            'ma10_vol_avg_chg_avg',
            'ma10_vol_avg_chg_avg_diff',

            'ma10_price_avg',
            'ma10_price_avg_chg',
            'ma10_price_avg_chg_avg',
            'ma10_price_avg_chg_avg_diff',

            'ma10_amount_flow_chg',
            'ma10_amount_flow_chg_avg',
            'ma10_amount_flow_chg_avg_diff',

            'ma10_close_ma_price_avg_chg',
        ]
        return list_keys

    def tuple_to_dict(self, tuple_data, list_keys):
        if tuple_data is not None and list_keys is not None and len(tuple_data) == len(list_keys):
            result = {}
            i = 0
            for key in list_keys:
                result[key] = tuple_data[i]
                i += 1
            return result
        else:
            return None

    def tuples_to_list_dict(self, tuples_data, list_keys):
        if tuples_data is not None and len(tuples_data) > 0 and list_keys is not None:
            result = []
            for tuple_data in tuples_data:
                dict_data = self.tuple_to_dict(tuple_data, list_keys)
                if dict_data is not None:
                    result.append(dict_data)
            return result
        else:
            return None

    def get_worth_buying_list_dict(self, security_code, size=20):
        tuples_data = self.get_worth_buying(security_code, size)
        result = self.tuples_to_list_dict(tuples_data, self.worth_buying_list_keys())
        return result


    def get_worth_buying(self, security_code, size=20):
        sql = """select 
                kline.the_date, 
                kline.amount, 
                kline.amount_chg, 
                kline.vol, 
                kline.open, 
                kline.open_low_chg, 
                kline.high, 
                kline.low, 
                kline.high_low_chg, 
                kline.high_close_chg, 
                kline.close, 
                kline.close_pre, 
                kline.close_chg, 
                kline.close_open_chg, 
                kline.close_open_chg, 
                kline.price_avg, 
                kline.close_price_avg_chg, 
                kline.price_avg_chg, 
                
                ma3.close_avg ma3_close_avg, 
                ma3.close_avg_chg ma3_close_avg_chg,
                ma3.close_avg_chg_avg ma3_close_avg_chg_avg, 
                ma3.close_avg_chg_avg_diff ma3_close_avg_chg_avg_diff, 
                
                ma3.amount_avg ma3_amount_avg, 
                ma3.amount_avg_chg ma3_amount_avg_chg, 
                ma3.amount_avg_chg_avg ma3_amount_avg_chg_avg, 
                ma3.amount_avg_chg_avg_diff ma3_amount_avg_chg_avg_diff,
                
                ma3.vol_avg ma3_vol_avg, 
                ma3.vol_avg_chg ma3_vol_avg_chg, 
                ma3.vol_avg_chg_avg ma3_vol_avg_chg_avg, 
                ma3.vol_avg_chg_avg_diff ma3_vol_avg_chg_avg_diff, 
                
                ma3.price_avg ma3_price_avg, 
                ma3.price_avg_chg ma3_price_avg_chg, 
                ma3.price_avg_chg_avg ma3_price_avg_chg_avg, 
                ma3.price_avg_chg_avg_diff ma3_price_avg_chg_avg_diff, 
                
                ma3.amount_flow_chg ma3_amount_flow_chg, 
                ma3.amount_flow_chg_avg ma3_amount_flow_chg_avg, 
                ma3.amount_flow_chg_avg_diff ma3_amount_flow_chg_avg_diff, 
                
                ma3.close_ma_price_avg_chg ma3_close_ma_price_avg_chg, 
                
                ma5.close_avg ma5_close_avg, 
                ma5.close_avg_chg ma5_close_avg_chg,
                ma5.close_avg_chg_avg ma5_close_avg_chg_avg, 
                ma5.close_avg_chg_avg_diff ma5_close_avg_chg_avg_diff, 
                
                ma5.amount_avg ma5_amount_avg, 
                ma5.amount_avg_chg ma5_amount_avg_chg, 
                ma5.amount_avg_chg_avg ma5_amount_avg_chg_avg, 
                ma5.amount_avg_chg_avg_diff ma5_amount_avg_chg_avg_diff,
                
                ma5.vol_avg ma5_vol_avg, 
                ma5.vol_avg_chg ma5_vol_avg_chg, 
                ma5.vol_avg_chg_avg ma5_vol_avg_chg_avg, 
                ma5.vol_avg_chg_avg_diff ma5_vol_avg_chg_avg_diff, 
                
                ma5.price_avg ma5_price_avg, 
                ma5.price_avg_chg ma5_price_avg_chg, 
                ma5.price_avg_chg_avg ma5_price_avg_chg_avg, 
                ma5.price_avg_chg_avg_diff ma5_price_avg_chg_avg_diff, 
                
                ma5.amount_flow_chg ma5_amount_flow_chg, 
                ma5.amount_flow_chg_avg ma5_amount_flow_chg_avg, 
                ma5.amount_flow_chg_avg_diff ma5_amount_flow_chg_avg_diff, 
                
                ma5.close_ma_price_avg_chg ma5_close_ma_price_avg_chg, 
                
                ma10.close_avg ma10_close_avg, 
                ma10.close_avg_chg ma10_close_avg_chg,
                ma10.close_avg_chg_avg ma10_close_avg_chg_avg, 
                ma10.close_avg_chg_avg_diff ma10_close_avg_chg_avg_diff, 
                
                ma10.amount_avg ma10_amount_avg, 
                ma10.amount_avg_chg ma10_amount_avg_chg, 
                ma10.amount_avg_chg_avg ma10_amount_avg_chg_avg, 
                ma10.amount_avg_chg_avg_diff ma10_amount_avg_chg_avg_diff,
                
                ma10.vol_avg ma10_vol_avg, 
                ma10.vol_avg_chg ma10_vol_avg_chg, 
                ma10.vol_avg_chg_avg ma10_vol_avg_chg_avg, 
                ma10.vol_avg_chg_avg_diff ma10_vol_avg_chg_avg_diff, 
                
                ma10.price_avg ma10_price_avg, 
                ma10.price_avg_chg ma10_price_avg_chg, 
                ma10.price_avg_chg_avg ma10_price_avg_chg_avg, 
                ma10.price_avg_chg_avg_diff ma10_price_avg_chg_avg_diff, 
                
                ma10.amount_flow_chg ma10_amount_flow_chg, 
                ma10.amount_flow_chg_avg ma10_amount_flow_chg_avg, 
                ma10.amount_flow_chg_avg_diff ma10_amount_flow_chg_avg_diff, 
                
                ma10.close_ma_price_avg_chg ma10_close_ma_price_avg_chg 
                
                from tquant_stock_day_kline kline 
                left join tquant_stock_average_line ma3 on kline.security_code = ma3.security_code and kline.the_date = ma3.the_date and ma3.ma = 3
                left join tquant_stock_average_line ma5 on kline.security_code = ma5.security_code and kline.the_date = ma5.the_date and ma5.ma = 5
                left join tquant_stock_average_line ma10 on kline.security_code = ma10.security_code and kline.the_date = ma10.the_date and ma10.ma = 10
                where kline.security_code = {security_code}
                order by kline.the_date desc limit {size}
                
                """
        tuple_data = self.query(sql.format(security_code=Utils.quotes_surround(security_code), size=size))
        return tuple_data