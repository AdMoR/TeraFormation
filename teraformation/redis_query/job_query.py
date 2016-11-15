# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
from redis import StrictRedis
import cPickle


def redis_job_query(keyword, city):

    r = StrictRedis(host='localhost', port=6379, db=0)
    all_keys = r.keys(keyword + ":" + city + "*")

    container = {}
    for key in all_keys:
        container[key] = cPickle.loads(r.get(key))

    return container


