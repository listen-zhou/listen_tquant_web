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
                     'status': self.sell,
                     'compare_price': None, 'compare_the_date': None, 'compare_close_open_chg': None,
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
                     'compare_price': None, 'compare_the_date': None, 'compare_close_open_chg': None,
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
                if(hold_info['status'] == self.sell):
                    # 当前空仓状态，则进行买入可行性搜索匹配
                    trade_flag = self.trade_buy_matching(hold_info, dict_item)
                    if trade_flag:
                        # 标记已买入
                        self.record_it(trade_records, hold_info, dict_item)
                else:
                    # 当前持仓，则进行卖出可行性搜索匹配
                    trade_flag = self.trade_sell_matching(hold_info, dict_item, security_code)
                    if trade_flag:
                        self.record_it(trade_records, hold_info, dict_item)
            return trade_records
        else:
            print('需要计算的数据为空，不能计算')
            return None

    def trade_buy_matching(self, hold_info, dict_item):
        if dict_item is not None:
            """
            买入条件：
            1.最低价为None时，为第一次寻求买入点
                遇到的第一个信息标记为等待买入持仓信息，对比价=收盘价，标记柱体颜色，时间，
            2如果当前持仓信息对比颜色为绿色
                2.1遇到红柱，即为翻转信号，买入，买入价=收盘价，对比价=收盘价，对比时间，对比颜色
                2.2遇到绿柱，且收盘价>对比价，即为翻转信号，买入，买入价=收盘价，对比价=收盘价，对比时间，对比颜色
                2.3遇到绿柱，且收盘价<对比价，则新低信号，更新对比价=收盘价，对比时间，对比颜色
            3如果当前持仓信息对比颜色为红柱
                3.1遇到红柱，且收盘价>对比价，则为新高信号，买入，更新买入价=收盘价，对比价=收盘价，对比时间，对比颜色
                3.2遇到红柱，且收盘价<对比价，则为新低信号，更新对比价=收盘价，对比颜色，对比时间
                3.3遇到绿柱，且收盘价>对比价，则为见顶信号，不买入，更新对比价=收盘价，对比时间，对比颜色，
                3.4遇到绿柱，且收盘价<对比价，则为新低信号，不买入，更新对比价=收盘价，对比时间，对比颜色，	
            hold_info = {'base_money': total_money,
                     'hold_hands': 0, 'left_money': total_money,
                     'status': self.sell,
                     'compare_price': None, 'compare_the_date': None, 'compare_close_open_chg': None,
                     'sell_price': None, 'sell_the_date': None,
                     'buy_price': None, 'buy_the_date': None,
                     'earnings': 0, 'diff_earnings': None, 'diff_days': None}
            """
            close = dict_item['close']
            the_date = dict_item['the_date']
            close_open_chg = dict_item['close_open_chg']
            # 现在是空仓待买入
            compare_price = hold_info['compare_price']
            # 最低价为None时，为第一次寻求买入点
            if compare_price is None:
                hold_info['compare_price'] = close
                hold_info['compare_the_date'] = the_date
                hold_info['compare_close_open_chg'] = close_open_chg
                print('寻求买入点时，对比价为空，则设置遇到的第一个更新为持仓对比信息', 'hold_info', hold_info)
                return False
            else:
                # 如果当前持仓信息对比颜色为绿色
                compare_close_open_chg = hold_info['compare_close_open_chg']
                if compare_close_open_chg <= 0:
                    # 遇到红柱，即为翻转信号，买入，买入价=收盘价，对比价=收盘价，对比时间，对比颜色
                    if (close_open_chg > 0) or (close_open_chg < 0 and close > compare_price):
                        # 计算买入花费
                        self.set_buy_hold_info(close, the_date, close_open_chg, hold_info)
                        return True
                    # 遇到绿柱，且收盘价<对比价，则新低信号，更新对比价=收盘价，对比时间，对比颜色
                    elif close_open_chg < 0 and close < compare_price:
                        # 设置对比信息
                        self.update_compare_info(close, the_date, close_open_chg, hold_info)
                        return False
                    else:
                        print('卖出状态时持仓信息为绿色时，没有匹配到买入条件，尴尬了')
                        # 设置对比信息
                        self.update_compare_info(close, the_date, close_open_chg, hold_info)
                        return False
                # 如果当前持仓信息对比颜色为红柱
                elif compare_close_open_chg > 0:
                    # 遇到红柱，且收盘价>对比价，则为新高信号，买入，更新买入价=收盘价，对比价=收盘价，对比时间，对比颜色
                    if close_open_chg > 0 and close > compare_price:
                        self.set_buy_hold_info(close, the_date, close_open_chg, hold_info)
                        return True
                    # 遇到红柱，且收盘价 < 对比价，则为新低信号，更新对比价 = 收盘价，对比颜色，对比时间
                    # 遇到绿柱，且收盘价 > 对比价，则为见顶信号，不买入，更新对比价 = 收盘价，对比时间，对
                    # 遇到绿柱，且收盘价 < 对比价，则为新低信号，不买入，更新对比价 = 收盘价，对比时间，对比颜色，
                    elif (close_open_chg > 0 and close < compare_price) \
                            or (close_open_chg < 0 and close > compare_price) \
                            or (close_open_chg < 0 and close < compare_price):
                        self.update_compare_info(close, the_date, close_open_chg, hold_info)
                        return False
                    else:
                        print('卖出状态时持仓信息为红色时，没有匹配到买入条件，尴尬了')
                        # 设置对比信息
                        self.update_compare_info(close, the_date, close_open_chg, hold_info)
                        return False
        else:
            return False

    def set_buy_hold_info(self, close, the_date, close_open_chg, hold_info):
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
        self.update_compare_info(close, the_date, close_open_chg, hold_info)

    def update_compare_info(self, close, the_date, close_open_chg, hold_info):
        # 设置对比信息
        hold_info['compare_price'] = close
        hold_info['compare_the_date'] = the_date
        hold_info['compare_close_open_chg'] = close_open_chg

    def set_sell_hold_info(self, close, the_date, close_open_chg, hold_info, security_code):
        sell_money = hold_info['hold_hands'] * 100 * close
        left_money = hold_info['left_money'] + sell_money
        hold_info['left_money'] = left_money
        hold_info['hold_hands'] = 0
        hold_info['sell_price'] = close
        hold_info['sell_the_date'] = the_date
        pre_earnings = hold_info['earnings']
        earnings = Utils.base_round(Utils.division_zero(left_money - hold_info['base_money'], hold_info['base_money']) * 100, 2)
        diff_earnings = earnings - pre_earnings
        hold_info['earnings'] = earnings
        hold_info['diff_earnings'] = diff_earnings
        hold_info['diff_days'] = self.get_diff_trade_days(hold_info['buy_the_date'], hold_info['sell_the_date'], security_code)
        hold_info['status'] = self.sell
        self.update_compare_info(close, the_date, close_open_chg, hold_info)

    def trade_sell_matching(self, hold_info, dict_item, security_code):
        if dict_item is not None:
            """
            卖出条件：
            1.如果当前持仓信息为红色
                1.1遇到绿柱，即为翻转新型号，卖出，卖出价=收盘价，期望价=收盘价，时间，标记颜色
                1.2遇到红柱，且收盘价<买入价，则新低信号，卖出，更新卖出价=收盘价，期望价=收盘价，时间，标记颜色
                1.3遇到红柱，且收盘价>买入价，则新高信号，继续持有，更新期望价=收盘价，时间，标记颜色
            2.如果当前持仓信息为率色
                绿色的持仓暂时没有，先不考虑，等待后续分析加入
            hold_info = {'base_money': total_money,
                     'hold_hands': 0, 'left_money': total_money,
                     'status': self.sell,
                     'compare_price': None, 'compare_the_date': None, 'compare_close_open_chg': None,
                     'sell_price': None, 'sell_the_date': None,
                     'buy_price': None, 'buy_the_date': None,
                     'earnings': 0, 'diff_earnings': None, 'diff_days': None}
            """
            close = dict_item['close']
            the_date = dict_item['the_date']
            close_open_chg = dict_item['close_open_chg']
            vol = dict_item['vol']
            # 现在是持仓待卖出
            compare_price = hold_info['compare_price']
            compare_close_open_chg = hold_info['compare_close_open_chg']
            # 当前收益跌幅
            current_rate = Utils.base_round(Utils.division_zero(close - hold_info['buy_price'], hold_info['buy_price']) * 100, 2)
            # 当前成交量幅度
            # current_vol_chg =
            # 如果当前持仓信息为红色
            if compare_close_open_chg > 0:
                # 遇到绿柱，即为翻转新型号，卖出，卖出价=收盘价，期望价=收盘价，时间，标记颜色
                if close_open_chg <= 0 and current_rate > 0:
                    self.set_sell_hold_info(close, the_date, close_open_chg, hold_info, security_code)
                    return True
                # 遇到红柱，且收盘价<期望价，则新低信号，卖出，更新卖出价=收盘价，期望价=收盘价，时间，标记颜色
                elif close_open_chg > 0 and close < compare_price:
                    self.set_sell_hold_info(close, the_date, close_open_chg, hold_info, security_code)
                    return True
                # 遇到红柱，且收盘价>买入价，则新高信号，继续持有，更新期望价=收盘价，时间，标记颜色
                elif close_open_chg > 0 and close > compare_price:
                    # 设置对比信息
                    self.update_compare_info(close, the_date, close_open_chg, hold_info)
                    return False
                else:
                    print('买入状态时持仓信息为红色时，没有匹配到卖出条件，尴尬了')
                    # 设置对比信息
                    self.update_compare_info(close, the_date, close_open_chg, hold_info)
                    return False
            # 如果当前持仓信息为绿色
            else:
                # 创新高，则更新最高价信息
                # 设置对比信息
                self.update_compare_info(close, the_date, close_open_chg, hold_info)
                return False
        else:
            return False



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
