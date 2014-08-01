#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xi cheng'

#Database operation module.

import time, uuid, functools, threaading, logging
#Dict object:

class Dict(dict):
    def __init__(self, names = (), values = (), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" %key)
    def __setattr__(self, key, value):
        self[key] = value
def next_id(t = None):
    if t is None:
        t = time.time()
    return '%015d%s000' %(int(t * 1000), uuid.uuid4().hex)

def _profiling(start, sql = ''):
    t = time.time() - start
    if t > 0.1:
        logging.warning('[PROFILING] [DB] %s: %s' %(t, sql))
    else:
        logging.info('[PROFILING] [DB] %s: %s' %(t, sql))

class DBError(Exception):
    pass
class MultiColumnsError(DBError):
    pass
class _LasyConnection(object):
    def __init__(self):
        self.connection = None
    def cursor(self):
        if self.connection is None:
            connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(connection)))
            self.connection = connection
        return self.connection.cursor()
    def commit(self):
        self.connection.commit()
    def rollback(self):
        self.connection.rollback()
    def cleanup(self):
        if self.connection:
            connection = self.connection
            self.connection = None
            logging.info('close connection <%s>...' % hex(id(connection)))
            connection.close()
class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transaction = 0
    def is_init(self):
        return not self.connection is None
    def init(self):
        logging.info('open lazy connection...')
        self.connection = _LasyConnection()
        self.transactions = 0
    def cleanup(self):
        self.connection.cleanup()
        self.connection = None
    def cursor(self):
        return self.connection.cursor()

_db_ctx = _DbCtx()
engine = None
class _Engine(object)
