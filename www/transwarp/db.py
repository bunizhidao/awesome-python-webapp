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
