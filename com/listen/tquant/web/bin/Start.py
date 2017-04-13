# coding: utf-8

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.wsgi import WSGIAdapter
import sys


from tornado.options import define, options

from com.listen.tquant.web.service.CheckStockIsWrothBuyingHandler import CheckStockIsWrothBuyingHandler
from com.listen.tquant.web.service.IndexHandler import IndexHandler
from com.listen.tquant.web.service.StockAverageLineModule import StockAverageLineModule
from com.listen.tquant.web.service.WebSocketHandler import WebSocketHandler

define('port', default=8000, help='run on the given port', type=int)

class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/average_line', CheckStockIsWrothBuyingHandler),
            (r'/average_line/ws', WebSocketHandler)
        ]

        print(os.path.dirname(__file__))
        print(os.path.join(os.path.dirname(__file__), os.path.pardir, 'templates'))
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), os.path.pardir, 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), os.path.pardir, 'static'),
            debug=True,
            autoreload=True,
            compiled_template_cache=False,
            static_hash_cache=False,
            serve_traceback=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
