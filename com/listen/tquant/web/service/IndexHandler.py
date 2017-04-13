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
        self.render('index.html', security_code='002466')

