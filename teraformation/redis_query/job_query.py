# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
from redis import StrictRedis
import enchant
#from geotext import GeoText


d = enchant.Dict("fr_FR")


def redis_job_query(keyword, city):

    r = StrictRedis(host='localhost', port=6379, db=0)
    all_keys = r.keys()
    container = None
    if keyword in all_keys:
        container = r.hget(keyword, city)

    return container


def query_with_tag(tag):
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

    return to_add


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


def clean_ugly_string(data):
    return [w for w in data.split() if d.check(w)]


def get_places(data):
    geo = GeoText(data[0])
    return geo.cities

