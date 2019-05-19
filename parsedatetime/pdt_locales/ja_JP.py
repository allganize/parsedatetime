# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import re
import time

from .base import *  # noqa

# don't use an unicode string
localeID = 'ja_JP'
dateSep = ['-']
timeSep = [':', 'h']
meridian = ['午前', '午後']
usesMeridian = True
uses24 = True
WeekdayOffsets = {}
MonthOffsets = {}
useAccuracy = False
tryRegexParsing = True

# always lowercase any lookup values - helper code expects that
Weekdays = [
    '月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日',
]

shortWeekdays = [
    '月', '火', '水', '木', '金', '土', '日',
]

Months = [
    '1月', '2月', '3月', '4月', '5月', '6月',
    '7月', '8月', '9月', '10月', '11月', '12月',
]

# We do not list 'mar' as a short name for 'mars' as it conflicts with
# the 'mar' of 'mardi'
shortMonths = [
    '1月', '2月', '3月', '4月', '5月', '6月',
    '7月', '8月', '9月', '10月', '11月', '12月',
]

# use the same formats as ICU by default
dateFormats = {
    'full': 'yyyy年MMMM月d日のEEEE',
    'long': 'yyyy MMMM d',
    'medium': 'yyyy MMM d',
    'short': 'yy-M-d'
}

timeFormats = {
    'full': 'hh:mm:ss a z',
    'long': 'h:mm:ss a z',
    'medium': 'h:mm:ss a',
    'short': 'h:mm a',
}

dp_order = ['y', 'm', 'd']

# Used to parse expressions like "in 5 hours"
numbers = {
    '零': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
}

decimal_mark = '.'

# this will be added to re_values later
units = {
    'seconds': ['秒'],
    'minutes': ['分'],
    'hours': ['時'],
    'days': ['日'],
    'weeks': ['週'],
    'months': ['月'],
    'years': ['年'],
}

# text constants to be used by later regular expressions
re_values = {
    'specials': '',
    'timeseparator': ":",
    'rangeseparator': '-',
    'daysuffix': '日',
    'meridian': '午前|夜明け|午後|昼|夜',
    'qunits': '時|分|秒|日|週|月|年',
    'now': ['今'],
}

# Used to adjust the returned date before/after the source
Modifiers = {
    '前々': -2,
    '先々': -2,
    '先': -1,
    '前': -1,
    '過去': -1,
    '次の': 1,
    '次': 1,
    '明後': 2,
    '後': 1,
    '再来': 2,
    '来': 1,
}

dayOffsets = {
    '明後日': 2,
    'あさって': 2,
    '明日': 1,
    '今日': 0,
    '昨日': -1,
    '前日': -1,
    '一昨日': -2,
    'おととい': -2,
}

# special day and/or times, i.e. lunch, noon, evening
# each element in the dictionary is a dictionary that is used
# to fill in any value to be replace - the current date/time will
# already have been populated by the method buildSources
re_sources = {
    '朝': {'hr': 6, 'mn': 0, 'sec': 0},
    '午前': {'hr': 9, 'mn': 0, 'sec': 0},
    '正午': {'hr': 12, 'mn': 0, 'sec': 0},
    '午後': {'hr': 13, 'mn': 0, 'sec': 0},
    '昼': {'hr': 13, 'mn': 0, 'sec': 0},
    '夜': {'hr': 19, 'mn': 0, 'sec': 0},
}

small = {
    '零': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
}

magnitude = {
    '百': 100,
    '千': 1000,
    '万': 10000,
    '億': 100000000,
    '兆': 1000000000000,
    '京': 10000000000000000,
}

ignore = (',', 'の')
cre_days = re.compile(rf'''\b((?P<qty>\d+)|(?P<nums>{'|'.join(numbers)}))\s*日\s*(?P<backforth>前|後)\b''', re.IGNORECASE)
cre_weeks = re.compile(rf'''\b\s*((?P<modifiers>{'|'.join(Modifiers)})|(?P<nums>{'|'.join(numbers)}))\s*週の?(?P<weekday>{'|'.join(Weekdays)})\b''', re.IGNORECASE)


def parseRegex(s, sourceTime):
    m = cre_days.match(s)
    if m:
        qty = m.group('qty')
        nums = m.group('nums')
        backforth = m.group('backforth') == '後'

        if qty:
            n = int(qty)
        elif nums:
            n = numbers[nums]

        multiplier = 1 if backforth else -1
        day_delta = n * multiplier
        dt = datetime.datetime.fromtimestamp(time.mktime(sourceTime)) + datetime.timedelta(days=day_delta)
        sourceTime = dt.timetuple()
        return sourceTime, True

    m = cre_weeks.match(s)
    if m:
        modifiers = m.group('modifiers')
        nums = m.group('nums')
        weekday = m.group('weekday')

        if modifiers:
            n = Modifiers[modifiers]
        elif nums:
            n = numbers[nums]

        if weekday:
            w = -sourceTime.tm_wday + Weekdays.index(weekday)
        else:
            w = 0

        day_delta = n*7 + w
        dt = datetime.datetime.fromtimestamp(time.mktime(sourceTime)) + datetime.timedelta(days=day_delta)
        sourceTime = dt.timetuple()
        return sourceTime, True

    return sourceTime, False
