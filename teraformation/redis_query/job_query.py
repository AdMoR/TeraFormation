# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
from redis import StrictRedis


def redis_job_query(keyword, city):

    r = StrictRedis(host='localhost', port=6379, db=0)
    all_keys = r.keys()

    if keyword in all_keys:
        container = r.hget(keyword, city)

    return container


def create_tag(tag):
    r = StrictRedis(host='localhost', port=6379, db=0)
    all_keys = r.keys()
    if tag in all_keys:
        return

    to_add = {}
    for key in all_keys:

        all_minor_keys = r.hkeys(key)

        for m_key in all_minor_keys:

            data = r.hget(key, m_key)
            matches = []

            for entry in data:
                # DO MAGIC WITH DATA
                if find_tag_in_entry(entry, tag):
                    matches.append(entry)

            if len(matches) > 0:
                if m_key not in to_add:
                    to_add[m_key] = []
                to_add[m_key].append(matches)

    if len(to_add) > 0:
        for k in to_add.keys():
            res = r.hget(tag, k)
            res.append(to_add[k])
            r.hset(tag, k, res)


def find_tag_in_entry(entry, tag):

    if type(entry) == str:
        return tag in entry
    elif type(entry) == dict:
        for k in entry.keys():
            if tag in k or tag in entry[k]:
                return True
        return False
    else:
        raise Exception("Type not handled")






