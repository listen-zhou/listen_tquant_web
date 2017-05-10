# conding: utf-8
import calendar
import decimal
from decimal import Decimal
from decimal import getcontext
import copy

import datetime


class Utils():

    @staticmethod
    def format_log_message(list):
        if list is not None and len(list) > 0:
            length = len(list)
            i = 0
            message = ''
            while i < length:
                message += '{0[' + str(i) + ']} '
                i += 1
            message = message.format(list)
            return message
        else:
            return None

    @staticmethod
    def quotes_surround(str):
        if str is not None:
            return "'" + str + "'"
        return str

    @staticmethod
    def base_round(val, n):
        if val is not None:
            val = Decimal(val, getcontext())
            return val.__round__(n)
        return None
    @staticmethod
    def base_round_zero(val, n):
        if val is not None:
            val = Decimal(val, getcontext())
        else:
            val = Decimal(0, getcontext())
        return val.__round__(n)

    @staticmethod
    def division(divisor, dividend):
        if divisor is not None and dividend is not None and dividend != 0 and dividend != Decimal(0):
            return divisor / dividend
        return None

    @staticmethod
    def division_zero(divisor, dividend):
        if divisor is not None:
            if dividend is not None and dividend != 0 and dividend != Decimal(0):
                return divisor / dividend
        return Decimal(0)

    @staticmethod
    def sum(list):
        if list is not None and len(list) > 0:
            total = Decimal(0)
            for item in list:
                if item is not None:
                    total += item
            return total
        return None

    @staticmethod
    def sum_zero(list):
        if list is not None and len(list) > 0:
            total = Decimal(0)
            for item in list:
                if item is not None:
                    total += item
            return total
        return Decimal(0)

    @staticmethod
    def average(list):
        if list is not None and len(list) > 0:
            total = Utils.sum(list)
            if total is not None:
                average = total / Decimal(len(list))
                return average
        return None

    @staticmethod
    def average_zero(list):
        if list is not None and len(list) > 0:
            total = Utils.sum(list)
            if total is not None:
                average = total / Decimal(len(list))
                return average
        return Decimal(0)

    @staticmethod
    def deepcopy_list(list):
        return copy.deepcopy(list)

    @staticmethod
    def get_week_day_num(the_date):
        if the_date is not None:
            year = the_date.year
            month = the_date.month
            day = the_date.day
            return calendar.weekday(year, month, day) + 1

    @staticmethod
    def get_amount_flow_css(price_avg_chg):
        if price_avg_chg is not None:
            if price_avg_chg >= 0:
                return 'm0'
            else:
                return 'l0'
        else:
            return ''

    @staticmethod
    def get_amount_flow_arrow(val, price_avg_chg):
        if val is not None and price_avg_chg is not None:
            if price_avg_chg > 0:
                if val > 100 and val < 150:
                    return '../static/img/stop2.gif'
                elif val >= 150 and val < 200:
                    return '../static/img/up2.gif'
                elif val >= 200:
                    return '../static/img/up1.gif'
                elif val == 100:
                    return ''
                elif val < 70 and val > 50:
                    return '../static/img/down4.gif'
                elif val <= 50 and val > 0:
                    return '../static/img/down3.gif'
                else:
                    return ''
            elif price_avg_chg < 0:
                if val > 100 and val < 150:
                    return '../static/img/stop3.gif'
                elif val >= 150 and val < 200:
                    return '../static/img/up4.gif'
                elif val >= 200:
                    return '../static/img/up3.gif'
                elif val == 100:
                    return ''
                elif val < 70 and val > 50:
                    return '../static/img/down2.gif'
                elif val <= 50 and val > 0:
                    return '../static/img/down1.gif'
                else:
                    return ''
            else:
                return ''

    @staticmethod
    def get_diff_arrow(val):
        if val is None or val == '':
            return ''
        if val > 0:
            return '../static/img/up2.gif'
        elif val < 0:
            return '../static/img/down2.gif'
        else:
            return '../static/img/stop2.gif'

    @staticmethod
    def get_css(val):
        if val is None or val == '':
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

    @staticmethod
    def json_default(val):
        if isinstance(val, datetime.date):
            return val.strftime('%m-%d')
        return val