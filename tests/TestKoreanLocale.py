# -*- coding: utf-8 -*-
"""
Test parsing of simple date and times using the Korean locale

Note: requires PyICU
"""
from __future__ import unicode_literals

import datetime
import sys
import time

from pytz import timezone

import parsedatetime as pdt
from parsedatetime import pdtContext
from . import utils

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class test(unittest.TestCase):
    @utils.assertEqualWithComparator
    def assertExpectedResult(self, result, check, **kwargs):
        return utils.compareResultByTimeTuplesAndFlags(result, check, **kwargs)

    def setUp(self):
        locale = 'ko_KR'
        self.ptc = pdt.Constants(locale, usePyICU=False)

        for x in self.ptc.cre_keys:
            self.ptc.cre_source[x] = self.ptc.cre_source[x].replace('\\b', '')
        self.cal = pdt.Calendar(self.ptc, version=pdt.VERSION_CONTEXT_STYLE)
        self.ptc.DOWParseStyle = 0

        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

        if self.ptc.localeID != locale:
            raise unittest.SkipTest(
                'Locale not set to ko_KR - check if PyICU is installed')

    def testTimes(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy,
            self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            self.yr, self.mth, self.dy, 23, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('2300', start), (target, pdtContext()))
        self.assertExpectedResult(
            self.cal.parse('23:00', start), (target, pdtContext()))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 11, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('1100', start), (target, pdtContext()))
        self.assertExpectedResult(
            self.cal.parse('11:00', start), (target, pdtContext()))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 7, 30, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('730', start), (target, pdtContext()))
        self.assertExpectedResult(
            self.cal.parse('0730', start), (target, pdtContext()))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('1730', start), (target, pdtContext()))
        self.assertExpectedResult(
            self.cal.parse('173000', start), (target, pdtContext()))

    def testDates(self):
        tz = timezone('Asia/Seoul')
        today = datetime.datetime.now(tz=tz).replace(hour=0, minute=0, second=0, microsecond=0)
        weekday = today.weekday()
        date_table = {
            '3일전': today + datetime.timedelta(days=-3),
            '3일 전': today + datetime.timedelta(days=-3),
            '3 일 전': today + datetime.timedelta(days=-3),
            '그제': today + datetime.timedelta(days=-2),
            '그저께': today + datetime.timedelta(days=-2),
            '이틀전': today + datetime.timedelta(days=-2),
            '이틀 전': today + datetime.timedelta(days=-2),
            '어제': today + datetime.timedelta(days=-1),
            '어저께': today + datetime.timedelta(days=-1),
            '전일': today + datetime.timedelta(days=-1),
            '오늘': today + datetime.timedelta(days=0),
            '금일': today + datetime.timedelta(days=0),
            '내일': today + datetime.timedelta(days=1),
            '명일': today + datetime.timedelta(days=1),
            '모레': today + datetime.timedelta(days=2),
            '재명일': today + datetime.timedelta(days=2),
            '명후일': today + datetime.timedelta(days=2),

            '월요일': today + datetime.timedelta(days=-weekday),
            '화요일': today + datetime.timedelta(days=-weekday + 1),
            '수요일': today + datetime.timedelta(days=-weekday + 2),
            '목요일': today + datetime.timedelta(days=-weekday + 3),
            '금요일': today + datetime.timedelta(days=-weekday + 4),
            '토요일': today + datetime.timedelta(days=-weekday + 5),
            '일요일': today + datetime.timedelta(days=-weekday + 6),

            '다음주': today + datetime.timedelta(days=7),
            '다음 주': today + datetime.timedelta(days=7),

            '지지난주 월요일': today + datetime.timedelta(days=-14 - weekday),
            '지지난주 화요일': today + datetime.timedelta(days=-14 - weekday + 1),
            '지지난주 수요일': today + datetime.timedelta(days=-14 - weekday + 2),
            '지지난주 목요일': today + datetime.timedelta(days=-14 - weekday + 3),
            '지지난주 금요일': today + datetime.timedelta(days=-14 - weekday + 4),
            '지지난주 토요일': today + datetime.timedelta(days=-14 - weekday + 5),
            '지지난주 일요일': today + datetime.timedelta(days=-14 - weekday + 6),
            '지난주 월요일': today + datetime.timedelta(days=-7 - weekday),
            '저번주 월요일': today + datetime.timedelta(days=-7 - weekday),
            '저번 주 월요일': today + datetime.timedelta(days=-7 - weekday),
            '지난주 화요일': today + datetime.timedelta(days=-7 - weekday + 1),
            '지난주 수요일': today + datetime.timedelta(days=-7 - weekday + 2),
            '지난주 목요일': today + datetime.timedelta(days=-7 - weekday + 3),
            '지난주 금요일': today + datetime.timedelta(days=-7 - weekday + 4),
            '지난주 토요일': today + datetime.timedelta(days=-7 - weekday + 5),
            '지난주 일요일': today + datetime.timedelta(days=-7 - weekday + 6),
            '다음주 월요일': today + datetime.timedelta(days=7 - weekday),
            '다음주 화요일': today + datetime.timedelta(days=7 - weekday + 1),
            '다음주 수요일': today + datetime.timedelta(days=7 - weekday + 2),
            '다음주 목요일': today + datetime.timedelta(days=7 - weekday + 3),
            '다음주 금요일': today + datetime.timedelta(days=7 - weekday + 4),
            '다음주 토요일': today + datetime.timedelta(days=7 - weekday + 5),
            '다음주 일요일': today + datetime.timedelta(days=7 - weekday + 6),
            '다다음주 월요일': today + datetime.timedelta(days=14 - weekday),
            '다다음주 화요일': today + datetime.timedelta(days=14 - weekday + 1),
            '다다음주 수요일': today + datetime.timedelta(days=14 - weekday + 2),
            '다다음주 목요일': today + datetime.timedelta(days=14 - weekday + 3),
            '다다음주 금요일': today + datetime.timedelta(days=14 - weekday + 4),
            '다다음주 토요일': today + datetime.timedelta(days=14 - weekday + 5),
            '다다음주 일요일': today + datetime.timedelta(days=14 - weekday + 6),
        }

        for dt_ko in date_table:
            dt, ctx = self.cal.parseDT(dt_ko, tzinfo=tz)
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            print(f'{dt_ko}:\t{dt}, {dt == date_table[dt_ko]}')
            self.assertEqual(date_table[dt_ko], dt)

    def testWeekDays(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy,
            self.hr, self.mn, self.sec).timetuple()

        o1 = self.ptc.CurrentDOWParseStyle
        o2 = self.ptc.DOWParseStyle

        # set it up so the current dow returns current day
        self.ptc.CurrentDOWParseStyle = True
        self.ptc.DOWParseStyle = 1

        for i in range(0, 7):
            dow = self.ptc.shortWeekdays[i]
            print(dow)

            result = self.cal.parse(dow, start)

            yr, mth, dy, hr, mn, sec, wd, yd, isdst = result[0]

            self.assertEqual(wd, i)

        self.ptc.CurrentDOWParseStyle = o1
        self.ptc.DOWParseStyle = o2


if __name__ == "__main__":
    unittest.main()
