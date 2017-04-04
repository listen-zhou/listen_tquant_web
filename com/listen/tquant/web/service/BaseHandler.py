# coding: utf-8

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys


from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html', table=5)

class TableHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # self.set_header('Access-Control-Allow-Origin', '*')
        # self.set_header('Access-Control-Allow-Methods', '*')
        # self.set_header('Access-Control-Max-Age', '1000')
        # self.set_header('Access-Control-Allow-Headers', '*')
        # self.set_header('Content-type', 'application/String')
        pass

    def post(self):
        table = 2
        try:
            table = self.get_argument('table')
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback)
        print('table', table)
        result = self.render_string('modules/table.html', table=table).decode('utf-8')
        print('result', str(result))
        self.write(result)
        self.set_status(200)

class TableModule(tornado.web.UIModule):
    def render(self, table):
        return self.render_string('modules/table.html', table=table)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    print(os.path.dirname(__file__))
    print(os.path.join(os.path.dirname(__file__), os.path.pardir, 'templates'))
    app = tornado.web.Application([(r'/login', LoginHandler),
                                   (r'/table', TableHandler)
                                   ],
                                  template_path=os.path.join(os.path.dirname(__file__), os.path.pardir, 'templates'),
                                  static_path=os.path.join(os.path.dirname(__file__), os.path.pardir, 'static'),
                                  debug=True,
                                  ui_modules={'table': TableModule}
                                  )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
