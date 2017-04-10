# coding: utf-8
import datetime
from tornado.websocket import WebSocketHandler
from com.listen.tquant.web.redis.StockAverageLineRedisService import StockAverageLineRedisService
from com.listen.tquant.web.service.CheckStockIsWrothBuyingHandler import CheckStockIsWrothBuyingHandler


class WebSocketHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print('open....')

    def on_message(self, message):
        while True:
            # 阻塞取出元素
            message = StockAverageLineRedisService.r.blpop(StockAverageLineRedisService.average_line_queue, 0)
            message = message[1].decode('utf-8')
            security_codes = message.split(',')
            security_code = str(security_codes[0])
            print(security_code)
            security_info = CheckStockIsWrothBuyingHandler.get_security_info(security_code)
            indexes = CheckStockIsWrothBuyingHandler.get_indexes()
            table_thead_dict = CheckStockIsWrothBuyingHandler.get_table_thead_dict()
            list_data = CheckStockIsWrothBuyingHandler.get_list_data(security_code, None, None, indexes)
            result = self.render_string('modules/average_list.html', table=list_data, indexes=indexes, thead_dict=table_thead_dict, update_date=datetime.datetime.now(), security_info=security_info)
            self.write_message(result)

    def on_close(self):
        print('close')