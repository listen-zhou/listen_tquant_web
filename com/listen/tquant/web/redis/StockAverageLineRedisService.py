# coding utf-8
import configparser
import os
import redis
import time

# https://github.com/ServiceStack/redis-windows
class StockAverageLineRedisService():
    config = configparser.ConfigParser()
    os.chdir('../config')
    config.read('redis.cfg')
    redis_section = config['redis']
    if redis_section:
        host = redis_section['redis.host']
        port = int(redis_section['redis.port'])
        db = redis_section['redis.db']
        average_line_queue = redis_section['redis.block.average.queue']
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        r = redis.Redis(connection_pool=pool)
    else:
        raise FileNotFoundError('redis.cfg redis section not found!!!')