# -*- coding: utf-8 -*-

import re
import pytz
import datetime

def get_year_from_tag(tag):
    m = re.search('(\d{4})年', tag.text)
    assert m != None
    return int(m.group(1))

def get_day_from_tag(tag):
    m = re.search('(\d{1,2})月\D*(\d{1,2})日\D*(\d{1,2})\：(\d{1,2})', tag.text)
    assert m != None
    mo = int(m.group(1))
    day = int(m.group(2))
    h = int(m.group(3))
    m = int(m.group(4))
    return (mo, day, h, m)

def create_datetime(yyyy, mo, day, h, m, timezone):
    dt = datetime.datetime(yyyy, mo, day, h, m)
    tz = pytz.timezone(timezone)
    date = tz.localize(dt)
    return date