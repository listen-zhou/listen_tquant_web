# coding: utf-8
import datetime
from tornado.websocket import WebSocketHandler
from com.listen.tquant.web.redis.StockAverageLineRedisService import StockAverageLineRedisService

class WebSocketHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print('open....')

    def on_message(self, message):
        print('server', message)
        while True:
            # 阻塞取出元素
            message = StockAverageLineRedisService.r.blpop(StockAverageLineRedisService.average_line_queue, 0)
            print(message[1])
            print(type(message[1]))
            message = message[1].decode('utf-8')
            security_codes = message.split(',')
            message = str(datetime.datetime.now()) + ' ' + str(security_codes[0]) + ' ' + str(security_codes[1])
            print(message)
            self.write_message(message)

    def on_close(self):
        print('close')