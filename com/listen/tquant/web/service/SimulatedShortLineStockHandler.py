# coding: utf-8
import datetime
from tornado.web import RequestHandler

from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils
from com.listen.tquant.web.model.ShortLineCondition import ShortLineCondition
from com.listen.tquant.web.model.PositionInfo import PositionInfo
import simplejson
class SimulatedShortLineStockHandler(RequestHandler):
    dbService = DbService()
    short_line_buy_condition = None
    short_line_sell_condition = None

    def post(self):
        security_code = self.get_argument('security_code', None)
        start_date = '2016-08-11'
        end_date = '2017-05-23'
        total_money = 20000
        position_info = PositionInfo(0, total_money, 0)
        if security_code is not None and start_date is not None and end_date is not None:
            result = self.get_stock_history_quotation(security_code, start_date, end_date)
            result = Utils.tuples_to_dicts(result, self.get_short_line_list_keys())
            result = Utils.append_week_day(result)
            self.combination_condition()
            trade_records = self.simulate_stock(total_money, position_info, self.short_line_buy_condition, self.short_line_sell_condition, result)
            result = {"rows": trade_records}
            result_json = simplejson.dumps(result, default=Utils.json_default)
            print('simulate_stock result: ', result_json)
            self.write(result_json)
        else:
            self.write('no data..')

    def simulate_stock(self, total_money, position_info, list_buy_condition, list_sell_condition, result):
        if result is not None and len(result) > 1:
            trade_records = []
            status = ''
            dict_status = None
            for i in range(len(result)):
                dict_item = result[i]
                if(status == '' or status == '卖'):
                    # 当前空仓状态，则进行买入可行性搜索匹配
                    trade_flag = self.trade_matching(list_buy_condition, dict_item)
                    if trade_flag:
                        # 标记已买入
                        status = '买'
                        self.trade_success(position_info, dict_item, status)
                        self.record_it(trade_records, status, total_money, position_info, dict_item)
                else:
                    # 当前持仓，则进行卖出可行性搜索匹配
                    trade_flag = self.trade_matching(list_sell_condition, dict_item)
                    if trade_flag:
                        status = '卖'
                        self.trade_success(position_info, dict_item, status)
                        self.record_it(trade_records, status, total_money, position_info, dict_item)
            return trade_records
        else:
            return None

    def record_it(self, trade_records, status, total_money, position_info, dict_item):
        earnings = self.calculate_earnings(total_money, position_info)
        dict_item['earnings'] = earnings
        dict_item['status'] = status
        dict_item['position_hands'] = position_info.position_hands
        dict_item['left_money'] = position_info.left_money
        dict_item['total_money'] = position_info.get_total_money()
        # dict_item['position_info'] = position_info
        trade_records.append(dict_item)
        print(status, dict_item)

    def calculate_earnings(self, total_money, position_info):
        position_hand_money = position_info.position_hands * 100 * position_info.close
        position_total_money = position_info.left_money + position_hand_money
        earnings = Utils.base_round_zero(Utils.division_zero(position_total_money - total_money, total_money) * 100, 2)
        return earnings

    def trade_success(self, position_info, dict_item, status):
        close = dict_item['close']
        one_hand = 100 * close
        if '买' == status:
            hands = int(position_info.left_money) // one_hand
            spend_money = hands * one_hand
            left_money = position_info.left_money - spend_money
            position_info.position_hands = hands
            position_info.left_money = left_money
        else:
            income_money = position_info.position_hands * one_hand
            position_info.position_hands = 0
            position_info.left_money = position_info.left_money + income_money
        position_info.close= close
        return position_info


    def trade_matching(self, list_condition, dict_item):
        list_flag = []
        for i in range(len(list_condition)):
            condition_item = list_condition[i]
            condition_name = condition_item.field_name
            condition_relation = condition_item.relation
            condition_value = condition_item.field_value
            value = dict_item[condition_name]
            flag = self.compare(value, condition_relation, condition_value)
            if flag == False:
                break
            else:
                list_flag.append(flag)
        if len(list_flag) == len(list_condition):
            return True
        else:
            return False


    def compare(self, value, relation, condition_value):
        if '=' == relation:
            return value == condition_value
        elif '>' == relation:
            return value > condition_value
        elif '>=' == relation:
            return value >= condition_value
        elif '<' == relation:
            return value <= condition_value
        elif '<=' == relation:
            return value <= condition_value
        else:
            return False

    @staticmethod
    def get_target_field_name():
        field_names = ['money_flow', 'close_chg', 'close_open_chg',
                       'price_avg_chg', 'price_avg_chg_3', 'price_avg_chg_5']
        return field_names

    @staticmethod
    def get_trade_direction():
        direction_names = ['buy', 'sell']
        return direction_names

    def combination_condition(self):
        self.short_line_buy_condition = []
        self.short_line_sell_condition = []
        for i in range(len(self.get_trade_direction())):
            trade_direction = self.get_trade_direction()[i]
            for j in range(len(self.get_target_field_name())):
                field_name = self.get_target_field_name()[j]
                relation_name = trade_direction + '_' + field_name + '_' + 'relation'
                relation_value = self.get_argument(relation_name, None)
                field_value_name = trade_direction + '_' + field_name + '_' + 'field_value'
                field_value_value = self.get_argument(field_value_name, None)
                if relation_value is not None and relation_value != '' and field_value_value is not None and field_value_value != '':
                    if 'buy' == trade_direction:
                        self.short_line_buy_condition.append(ShortLineCondition(field_name, relation_value, Utils.str_to_decimal(field_value_value, 2)))
                    elif 'sell' == trade_direction:
                        self.short_line_sell_condition.append(ShortLineCondition(field_name, relation_value, Utils.str_to_decimal(field_value_value, 2)))


        # list_condition.append(ShortLineCondition('money_flow', '<', 100))

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
