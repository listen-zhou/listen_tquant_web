# coding: utf-8
from datetime import datetime

from tornado.web import RequestHandler
from com.listen.tquant.web.dbservice.Service import DbService
from com.listen.tquant.web.utils.Utils import Utils

import json
import simplejson

class WorthBuyingHandler(RequestHandler):
    dbService = DbService()

    def post(self):
        security_code = self.get_argument('security_code')
        size = self.get_argument('size', '0')
        if security_code is not None:
            result = self.dbService.get_worth_buying_list_dict(security_code, size)
            result = {"rows": result}
            result_json = simplejson.dumps(result, default=Utils.json_default)
            print('get_worth_buying_list_dict result: ', result_json)
            self.write(result_json)
        else:
            self.write("no data!!!")

    def get(self):
        result = self.dbService.get_worth_buying_list_dict_codes()
        if result is not None:
            result_json = simplejson.dumps(result)
            print('get_worth_buying_list_dict_codes result:', result_json)
            self.write(result_json)
        else:
            self.write('no data!!!')

