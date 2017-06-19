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
                     'hold_hands': 0, 'left_money': total_money,
                     'status': self.sell, 'first_buy_price': None,
                     'current_price_avg_chg': None, 'fall_times': 0,
                     'sell_price': None, 'sell_the_date': None,
                     'buy_price': None, 'buy_the_date': None,
                     'earnings': 0, 'diff_earnings': None, 'diff_days': None}
        result_dict = {}
        if security_code is not None \
                and start_date is not None and start_date != '' \
                and end_date is not None:
            result = self.get_stock_history_quotation(security_code, start_date, end_date)
            result = Utils.tuples_to_dicts(result, self.get_short_line_list_keys())
            result = Utils.append_week_day(result)
            trade_records = self.simulate_stock(hold_info, result, security_code)
            result_dict['rows'] = trade_records
            result_dict['status'] = 'success'
            result_json = simplejson.dumps(result_dict, default=Utils.json_default)
            print('simulate_stock result: ', result_json)
            self.write(result_json)
        else:
            result_dict['status'] = 'faliure'
            result_dict['message'] = '股票代码或开始时间为空，请先设置'
            result_json = simplejson.dumps(result_dict, default=Utils.json_default)
            print('股票代码为空，不能计算，simulate_stock result: ', result_json)
            self.write(result_json)


    def simulate_stock(self, hold_info, result, security_code):
        """
        hold_info = {'base_money': total_money,
                     'hold_hands': 0, 'left_money': total_money,
                     'status': self.sell,
                     'current_price_avg_chg': None, 
                     'sell_price': None, 'sell_the_date': None,
                     'buy_price': None, 'buy_the_date': None,
                     'earnings': 0, 'diff_earnings': None, 'diff_days': None}
        :param hold_info: 
        :param result: 
        :return: 
        """
        if result is not None and len(result) > 1:
            trade_records = []
            for i in range(len(result)):
                dict_item = result[i]
                trade_flag = self.trade_matching(hold_info, dict_item, security_code)
                if trade_flag:
                    self.record_it(trade_records, hold_info, dict_item)
            return trade_records
        else:
            print('需要计算的数据为空，不能计算')
            return None

    def trade_matching(self, hold_info, dict_item, security_code):
        if dict_item is not None:
            """
            买入条件：收幅>=0，日均幅-升，即当前的日均幅小于后一天的日均幅，无论红绿颜色	
            hold_info = {'base_money': total_money,
                     'hold_hands': 0, 'left_money': total_money,
                     'status': self.sell,
                     'current_price_avg_chg': None, 
                     'sell_price': None, 'sell_the_date': None,
                     'buy_price': None, 'buy_the_date': None,
                     'earnings': 0, 'diff_earnings': None, 'diff_days': None}
            """
            close = dict_item['close']

            the_date = dict_item['the_date']
            close_chg = dict_item['close_chg']
            close_open_chg = dict_item['close_open_chg']
            price_avg_chg = dict_item['price_avg_chg']

            current_price_avg_chg = hold_info['current_price_avg_chg']
            # 如果现在是空仓待买入
            if hold_info['status'] == self.sell:
                # 买入条件：收幅>=0，日均幅-升，即当前的日均幅小于后一天的日均幅，无论红绿颜色
                if current_price_avg_chg is not None \
                        and close_chg >= 0 and current_price_avg_chg < price_avg_chg \
                        and close_open_chg >= 0:
                    # 遇到红柱，即为翻转信号，买入，买入价=收盘价，对比价=收盘价，对比时间，对比颜色
                    self.set_buy_hold_info(close, the_date, price_avg_chg, hold_info)
                    return True
                else:
                    hold_info['current_price_avg_chg'] = price_avg_chg
                    return False
            elif hold_info['status'] == self.buy:
                buy_price = hold_info['buy_price']
                fall_times = hold_info['fall_times']
                if buy_price > close:
                    fall_times += 1
                else:
                    fall_times = 0
                hold_info['fall_times'] = fall_times
                # 在下跌时，判断可以承受的割肉率，是否在可承受的范围内
                current_earnings = Utils.base_round(Utils.division_zero(close - buy_price, buy_price) * 100, 2)
                # 卖出条件：收幅 < 0， 日均幅 - 降，即当前日均幅大于后一天的日均幅，无论红绿颜色
                if (current_price_avg_chg is not None
                    and close_chg < 0 and current_price_avg_chg >= price_avg_chg and current_earnings > 0) \
                        or (close_open_chg <= 0 and current_earnings >= 0) or current_earnings <= -5 or fall_times >= 3:
                    self.set_sell_hold_info(close, the_date, price_avg_chg, hold_info, security_code)
                    return True
                else:
                    hold_info['current_price_avg_chg'] = price_avg_chg
                    return False
        else:
            return False

    def set_buy_hold_info(self, close, the_date, price_avg_chg, hold_info):
        one_hand = 100 * close
        hands = int(hold_info['left_money']) // one_hand
        spend_money = hands * one_hand
        left_money = hold_info['left_money'] - spend_money
        hold_info['hold_hands'] = hands
        hold_info['left_money'] = left_money
        # 设置买入信息
        hold_info['status'] = self.buy
        hold_info['buy_price'] = close
        hold_info['buy_the_date'] = the_date
        hold_info['current_price_avg_chg'] = price_avg_chg
        first_buy_price = hold_info['first_buy_price']
        if first_buy_price is None :
            hold_info['first_buy_price'] = close
        hold_info['fall_times'] = 0

    def set_sell_hold_info(self, close, the_date, price_avg_chg, hold_info, security_code):
        sell_money = hold_info['hold_hands'] * 100 * close
        left_money = hold_info['left_money'] + sell_money
        hold_info['left_money'] = left_money
        hold_info['hold_hands'] = 0
        hold_info['sell_price'] = close
        hold_info['sell_the_date'] = the_date
        pre_earnings = hold_info['earnings']
        earnings = Utils.base_round(Utils.division_zero(close - hold_info['first_buy_price'], hold_info['first_buy_price']) * 100, 2)
        diff_earnings = Utils.base_round(Utils.division_zero(close - hold_info['buy_price'], hold_info['buy_price']) * 100, 2)
        hold_info['earnings'] = earnings
        hold_info['diff_earnings'] = diff_earnings
        hold_info['diff_days'] = self.get_diff_trade_days(hold_info['buy_the_date'], hold_info['sell_the_date'], security_code)
        hold_info['status'] = self.sell
        hold_info['current_price_avg_chg'] = price_avg_chg


    def record_it(self, trade_records, hold_info, dict_item):
        # 如果是卖出成交，则计算收益率，买入则不计算
        if hold_info['status'] == self.sell:
            dict_item['earnings'] = hold_info['earnings']
            dict_item['total_money'] = hold_info['left_money']
            dict_item['diff_days'] = hold_info['diff_days']
            dict_item['diff_earnings'] = hold_info['diff_earnings']
        else:
            dict_item['hold_hands'] = hold_info['hold_hands']
            dict_item['total_money'] = hold_info['left_money'] + hold_info['hold_hands'] * 100 * hold_info['buy_price']
            # dict_item['diff_days'] = Utils.get_diff_days(hold_info['sell_the_date'], hold_info['buy_the_date'])
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
