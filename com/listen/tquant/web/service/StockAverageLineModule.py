# coding: utf-8

import tornado.web

class StockAverageLineModule(tornado.web.UIModule):
    def render(self, table):
        return self.render_string('modules/table.html', table=table).decode('utf-8')
