# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import re
import time

from .base import *  # noqa


# don't use an unicode string
localeID = 'ko_KR'
dateSep = ['-']
timeSep = [':', 'h']
meridian = ['오전', '오후']
usesMeridian = True
uses24 = True
WeekdayOffsets = {}
MonthOffsets = {}
useAccuracy = False
tryRegexParsing = True

# always lowercase any lookup values - helper code expects that
Weekdays = [
    '월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일',
]

shortWeekdays = [
    '월', '화', '수', '목', '금', '토', '일',
]

Months = [
    '1월', '2월', '3월', '4월', '5월', '6월',
    '7월', '8월', '9월', '10월', '11월', '12월',
]

# We do not list 'mar' as a short name for 'mars' as it conflicts with
# the 'mar' of 'mardi'
shortMonths = [
    '1월', '2월', '3월', '4월', '5월', '6월',
    '7월', '8월', '9월', '10월', '11월', '12월',
]

# use the same formats as ICU by default
dateFormats = {
    'full': 'yyyy년 MMMM월 d일 EEEE',
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
    '영': 0,
    '하나': 1,
    '한': 1,
    '일': 1,
    '둘': 2,
    '두': 2,
    '이': 2,
    '셋': 3,
    '세': 3,
    '삼': 3,
    '넷': 4,
    '네': 4,
    '사': 4,
    '다섯': 5,
    '오': 5,
    '여섯': 6,
    '육': 6,
    '일곱': 7,
    '칠': 7,
    '여덟': 8,
    '팔': 8,
    '아홉': 9,
    '구': 9,
    '열': 10,
    '십': 10,
}

decimal_mark = '.'

# this will be added to re_values later
units = {
    'seconds': ['초'],
    'minutes': ['분'],
    'hours': ['시'],
    'days': ['일'],
    'weeks': ['주'],
    'months': ['월'],
    'years': ['년'],
}

# text constants to be used by later regular expressions
re_values = {
    'specials': '',
    'timeseparator': ":",
    'rangeseparator': '-',
    'daysuffix': '일',
    'meridian': '오전|새벽|오후|낮|밤',
    'qunits': '시|분|초|일|주|월|년',
    'now': ['지금', '바로'],
}

# Used to adjust the returned date before/after the source
Modifiers = {
    '지지난': -2,
    '저저번': -2,
    '지난': -1,
    '저번': -1,
    '이번': 0,
    '다다음': 2,
    '다음': 1,
}

dayOffsets = {
    '모레': 2,
    '재명일': 2,
    '명후일': 2,
    '이틀후': 2,
    '이틀 후': 2,
    '내일': 1,
    '명일': 1,
    '오늘': 0,
    '금일': 0,
    '어제': -1,
    '어저께': -1,
    '전일': -1,
    '그제': -2,
    '그저께': -2,
    '이틀전': -2,
    '이틀 전': -2,
    '사흘전': -3,
    '사흘 전': -3,
    '나흘전': -4,
    '나흘 전': -4,
}

# special day and/or times, i.e. lunch, noon, evening
# each element in the dictionary is a dictionary that is used
# to fill in any value to be replace - the current date/time will
# already have been populated by the method buildSources
re_sources = {
    '아침': {'hr': 6, 'mn': 0, 'sec': 0},
    '오전': {'hr': 9, 'mn': 0, 'sec': 0},
    '정오': {'hr': 12, 'mn': 0, 'sec': 0},
    '점심': {'hr': 12, 'mn': 0, 'sec': 0},
    '오후': {'hr': 13, 'mn': 0, 'sec': 0},
    '낮': {'hr': 13, 'mn': 0, 'sec': 0},
    '저녁': {'hr': 19, 'mn': 0, 'sec': 0},
    '밤': {'hr': 21, 'mn': 0, 'sec': 0},
    '자정': {'hr': 0, 'mn': 0, 'sec': 0},
}

small = {
    '영': 0,
    '하나': 1,
    '한': 1,
    '일': 1,
    '둘': 2,
    '두': 2,
    '이': 2,
    '셋': 3,
    '세': 3,
    '삼': 3,
    '넷': 4,
    '네': 4,
    '사': 4,
    '다섯': 5,
    '오': 5,
    '여섯': 6,
    '육': 6,
    '일곱': 7,
    '칠': 7,
    '여덟': 8,
    '팔': 8,
    '아홉': 9,
    '구': 9,
    '열': 10,
    '십': 10,
}

magnitude = {
    '백': 100,
    '천': 1000,
    '만': 10000,
    '억': 100000000,
    '조': 1000000000000,
    '경': 10000000000000000,
}

ignore = (',', )
cre_pattern = re.compile(r'(?P<qty>\d+)\s*일\s*(?P<backforth>전|후)', re.IGNORECASE)


def parseRegex(s, sourceTime):
    m = cre_pattern.match(s)
    if m:
        qty = int(m.group('qty'))
        backforth = m.group('backforth') == '후'
        multiplier = 1 if backforth else -1
        dt = datetime.datetime.fromtimestamp(time.mktime(sourceTime)) + datetime.timedelta(days=qty * multiplier)
        sourceTime = dt.timetuple()
        return sourceTime, True
    return sourceTime, False
