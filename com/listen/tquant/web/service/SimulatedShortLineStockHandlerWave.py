# coding: utf-8
import datetime
from tornado.web import RequestHandler

from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils
from com.listen.tquant.web.model.ShortLineCondition import ShortLineCondition
from com.listen.tquant.web.model.PositionInfo import PositionInfo
import simplejson
class SimulatedShortLineStockHandlerWave(RequestHandler):
    dbService = DbService()

    buy = 'buy'
    sell = 'sell'

    def post(self):
        security_code = self.get_argument('simulated_security_code', None)
        start_date = self.get_argument('start_date', None)
        end_date = self.get_argument('end_date', Utils.format_yyyy_mm_dd(datetime.datetime.now()))
        total_money = int(self.get_argument('total_money', 20000))
        print('security_code', security_code, 'start_date', start_date, 'end_date', end_date)
        hold_info = {'base_money': total_money,
                     'hold_hands': 0, 'left_money': total_money, 'earnings': 0,
                     'status': self.sell,
                     'max_price': None, 'max_the_date': None,
                     'sell_price': None, 'sell_the_date': None,
                     'min_price': None, 'min_the_date': None,
                     'buy_price': None, 'buy_the_date': None}
        result_dict = {}
        if security_code is not None \
                and start_date is not None and start_date != '' \
                and end_date is not None:
            result = self.get_stock_history_quotation(security_code, start_date, end_date)
            result = Utils.tuples_to_dicts(result, self.get_short_line_list_keys())
            result = Utils.append_week_day(result)
            trade_records = self.simulate_stock(hold_info, result)
            result_dict['rows'] = trade_records
            result_dict['status'] = 'success'
            result_json = simplejson.dumps(result_dict, default=Utils.json_default)
            # print('simulate_stock result: ', result_json)
            self.write(result_json)
        else:
            result_dict['status'] = 'faliure'
            result_dict['message'] = '股票代码或开始时间为空，请先设置'
            result_json = simplejson.dumps(result_dict, default=Utils.json_default)
            print('股票代码为空，不能计算，simulate_stock result: ', result_json)
            self.write(result_json)


    def simulate_stock(self, hold_info, result):
        """
        hold_info = {'base_money': total_money,
                     'hold_hands': 0, 'left_money': total_money, 'earnings': 0,
                     'status': self.sell,
                     'max_price': None, 'max_the_date': None,
                     'sell_price': None, 'sell_the_date': None,
                     'min_price': None, 'min_the_date': None,
                     'buy_price': None, 'buy_the_date': None}
        :param hold_info: 
        :param result: 
        :return: 
        """
        if result is not None and len(result) > 1:
            trade_records = []
            for i in range(len(result)):
                dict_item = result[i]
                if(hold_info['status'] == self.sell):
                    # 当前空仓状态，则进行买入可行性搜索匹配
                    trade_flag = self.trade_buy_matching(hold_info, dict_item)
                    if trade_flag:
                        # 标记已买入
                        self.record_it(trade_records, hold_info, dict_item)
                else:
                    # 当前持仓，则进行卖出可行性搜索匹配
                    trade_flag = self.trade_sell_matching(hold_info, dict_item)
                    if trade_flag:
                        self.record_it(trade_records, hold_info, dict_item)
            return trade_records
        else:
            print('需要计算的数据为空，不能计算')
            return None

    def trade_buy_matching(self, hold_info, dict_item):
        if dict_item is not None:
            close = dict_item['close']
            the_date = dict_item['the_date']
            # 现在是空仓待买入
            min_price = hold_info['min_price']
            # 如果空仓时最低价为空，则设置第一个遇到的收盘价为最低价
            if min_price is None:
                min_price = close
                hold_info['min_price'] = min_price
                hold_info['min_the_date'] = the_date
                print('卖出状态需求买入机会时，遇到第一个，设置为最低信息', 'min_price', min_price, 'min_the_date', hold_info['min_the_date'])
                return False
            else:
                # 如果空仓时最低价不为空，则对比遇到的每一个收盘价，
                # 如果最低价>收盘价，创新低，则更新持仓中的最低价为收盘价
                close_open_chg = dict_item['close_open_chg']
                if close_open_chg > 0:
                    # 如果最低价<收盘价，止跌反弹，见底信号则买入，更新持仓中的买入价
                    print('最低价止跌翻转，达到买入条件', 'min_price', min_price, 'min_the_date', hold_info['min_the_date'],
                          'close', close, the_date)
                    one_hand = 100 * close
                    hands = int(hold_info['left_money']) // one_hand
                    spend_money = hands * one_hand
                    left_money = hold_info['left_money'] - spend_money

                    hold_info['buy_price'] = close
                    hold_info['buy_the_date'] = the_date
                    hold_info['hold_hands'] = hands
                    hold_info['left_money'] = left_money
                    hold_info['status'] = self.buy
                    # 买入时设置最高价为当前的收盘价
                    hold_info['max_price'] = close
                    hold_info['max_the_date'] = the_date
                    return True
                else:
                    print('最低价创新低，没有达到止跌翻转条件', 'min_price', min_price, 'min_the_date', hold_info['min_the_date'], 'close', close, the_date)
                    hold_info['min_price'] = close
                    hold_info['min_the_date'] = the_date
                    return False
        else:
            return False

    def trade_sell_matching(self, hold_info, dict_item):
        if dict_item is not None:
            close = dict_item['close']
            the_date = dict_item['the_date']
            # 现在是持仓待卖出
            max_price = hold_info['max_price']
            close_open_chg = dict_item['close_open_chg']
            # 最高止盈即逢收盘价<最高价，或者收开幅即收盘价<开盘价，高开低走，即见顶信号，则卖出
            # 买入价如果小于收盘价，则说明有盈利，且为(绿柱或收盘价<最高价，说明上升通道临时关闭)，应立即卖出，否则继续持有，等待盈利卖出
            # 当前收益跌幅
            current_rate = Utils.base_round(Utils.division_zero(close - hold_info['buy_price'], hold_info['buy_price']) * 100, 2)
            if (close_open_chg < 0.3 and (current_rate > 0 or current_rate < -3)) or (close_open_chg <= -3):
                print('最高价止盈翻转，或收开幅小于0变绿柱，达到卖出条件',
                      'buy_price', hold_info['buy_price'], 'buy_the_date', hold_info['buy_the_date'],
                      'max_price', hold_info['max_price'], 'max_the_date', hold_info['max_the_date'],
                      'close', close, the_date, 'close_open_chg', close_open_chg)
                sell_money = hold_info['hold_hands'] * 100 * close
                left_money = hold_info['left_money'] + sell_money
                hold_info['left_money'] = left_money
                hold_info['hold_hands'] = 0
                hold_info['sell_price'] = close
                hold_info['sell_the_date'] = the_date
                hold_info['status'] = self.sell
                # 卖出时设置最低价为卖出价
                hold_info['min_price'] = close
                hold_info['min_the_date'] = the_date
                return True
            else:
                # 创新高，则更新最高价信息
                print('最高价创新高，没有达到止盈翻转条件', 'max_price', hold_info['max_price'], 'max_the_date', hold_info['max_the_date'],
                      'close', close, the_date)
                hold_info['max_price'] = close
                hold_info['max_the_date'] = the_date
                return False
        else:
            return False



    def record_it(self, trade_records, hold_info, dict_item):
        # 如果是卖出成交，则计算收益率，买入则不计算
        if hold_info['status'] == self.sell:
            earnings = Utils.base_round(
                Utils.division_zero(hold_info['left_money'] - hold_info['base_money'], hold_info['base_money']) * 100,
                2)
            dict_item['earnings'] = earnings
            dict_item['total_money'] = hold_info['left_money']
            dict_item['diff_days'] = Utils.get_diff_days(hold_info['buy_the_date'], hold_info['sell_the_date'])
            pre_index = len(trade_records) - 2
            pre_earnings = 0
            earnings_diff = 0
            if pre_index >= 0:
                pre_earnings = trade_records[pre_index]['earnings']
            earnings_diff = dict_item['earnings'] - pre_earnings
            dict_item['earnings_diff'] = earnings_diff
        else:
            dict_item['hold_hands'] = hold_info['hold_hands']
            dict_item['total_money'] = hold_info['left_money'] + hold_info['hold_hands'] * 100 * hold_info['buy_price']
            dict_item['diff_days'] = Utils.get_diff_days(hold_info['sell_the_date'], hold_info['buy_the_date'])
        dict_item['status'] = hold_info['status']
        trade_records.append(dict_item)

    def get_diff_trade_days(self, the_date1, the_date2, security_code):
        if the_date1 is None or the_date2 is None:
            return 0
        else:
            if (isinstance(the_date1, datetime.date) or isinstance(the_date1, datetime.datetime)) \
                    and (isinstance(the_date2, datetime.date) or isinstance(the_date2, datetime.datetime)):
                sql = "select count(*) from tquant_stock_history_quotation where security_code = {security_code} and the_date >= {start_date} and the_date <= {end_date}"
                sql = sql.format(
                    security_code=Utils.quotes_surround(security_code),
                    start_date=Utils.quotes_surround(the_date1.strftime('%Y-%m-%d')),
                    end_date=Utils.quotes_surround(the_date2.strftime('%Y-%m-%d')))
                count_tuples = self.dbService.query(sql)
                if count_tuples is not None:
                    count = count_tuples[0][0]
                    return count - 1
                else:
                    return 0
            else:
                return 0


    @staticmethod
    def get_target_field_name():
        field_names = ['money_flow', 'close_chg', 'close_open_chg', 'close_price_avg_chg',
                       'close_10_price_avg_chg',
                       'price_avg_chg', 'price_avg_chg_3', 'price_avg_chg_5',
                       'price_avg_chg_10', 'price_avg_chg_10_avg']
        return field_names

    @staticmethod
    def get_short_line_list_keys():
        list_keys = ['the_date',
                     'open', 'high', 'low',
                     'close',
                     'vol_chg', 'close_chg', 'close_open_chg', 'close_price_avg_chg',
                     'price_avg_chg',
                     'price_avg_chg_3',
                     'price_avg_chg_5',
                     'price_avg_chg_10', 'close_10_price_avg_chg',
                     'price_avg_chg_10_avg', 'price_avg_chg_10_avg_diff',
                     'money_flow',
                     'vol', 'amount', 'price_avg', 'price_avg_3', 'price_avg_5', 'price_avg_10']
        return list_keys

    def get_stock_history_quotation(self, security_code, start_date, end_date):
        if security_code is not None and start_date is not None:
            if end_date is None or end_date == '':
                today = datetime.datetime.today()
                end_date = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
            sql = "select the_date, " \
                  "open, high, low, " \
                  "close, " \
                  "vol_chg, " \
                  "close_chg, close_open_chg, close_price_avg_chg, " \
                  "price_avg_chg, " \
                  "price_avg_chg_3, " \
                  "price_avg_chg_5, " \
                  "price_avg_chg_10, close_10_price_avg_chg, " \
                  "price_avg_chg_10_avg, price_avg_chg_10_avg_diff, " \
                  "money_flow, " \
                  "vol, amount, price_avg, price_avg_3, price_avg_5, price_avg_10 " \
                  "from tquant_stock_history_quotation " \
                  "where security_code = {security_code} " \
                  "and the_date >= {start_date} and the_date <= {end_date} " \
                  "order by the_date asc "
            sql = sql.format(security_code=Utils.quotes_surround(security_code),
                             start_date=Utils.quotes_surround(start_date),
                             end_date=Utils.quotes_surround(end_date)
                             )
            result = self.dbService.query(sql)
            return result
