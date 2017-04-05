# coding: utf-8

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys


from tornado.options import define, options

from com.listen.tquant.web.dbservice.Service import DbService


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        dbService = DbService()

        sql = "select the_date from tquant_calendar_info order by the_date desc limit 20"
        tuple_the_date = dbService.query(sql)
        if tuple_the_date is not None and len(tuple_the_date) > 0:
            start_date = tuple_the_date[len(tuple_the_date) - 1][0].strftime('%Y-%m-%d')
            end_date= tuple_the_date[0][0].strftime('%Y-%m-%d')
        else:
            start_date = '2017-03-05'
            end_date = '2017-04-05'

        self.render('index.html',
                    start_date=start_date,
                    end_date=end_date
                    )

