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
        locale = 'ja_JP'
        self.ptc = pdt.Constants(locale, usePyICU=False)

        for x in self.ptc.cre_keys:
            self.ptc.cre_source[x] = self.ptc.cre_source[x].replace('\\b', '')
        self.cal = pdt.Calendar(self.ptc, version=pdt.VERSION_CONTEXT_STYLE)
        self.ptc.DOWParseStyle = 0

        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

        if self.ptc.localeID != locale:
            raise unittest.SkipTest(
                'Locale not set to ja_JP - check if PyICU is installed')

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
        tz = timezone('Asia/Tokyo')
        tz = tz.localize(datetime.datetime.now()).tzinfo
        today = datetime.datetime.now(tz=tz).replace(hour=0, minute=0, second=0, microsecond=0)
        weekday = today.weekday()
        date_table = {
            '3日前': today + datetime.timedelta(days=-3),
            '3日後': today + datetime.timedelta(days=3),
            '一昨日': today + datetime.timedelta(days=-2),
            '二日前': today + datetime.timedelta(days=-2),
            'おととい': today + datetime.timedelta(days=-2),
            '昨日': today + datetime.timedelta(days=-1),
            '前日': today + datetime.timedelta(days=-1),
            '今日': today + datetime.timedelta(days=0),
            '明日': today + datetime.timedelta(days=1),
            '明後日': today + datetime.timedelta(days=2),
            'あさって': today + datetime.timedelta(days=2),
            '月曜日': today + datetime.timedelta(days=-weekday),
            '火曜日': today + datetime.timedelta(days=-weekday + 1),
            '水曜日': today + datetime.timedelta(days=-weekday + 2),
            '木曜日': today + datetime.timedelta(days=-weekday + 3),
            '金曜日': today + datetime.timedelta(days=-weekday + 4),
            '土曜日': today + datetime.timedelta(days=-weekday + 5),
            '日曜日': today + datetime.timedelta(days=-weekday + 6),

            '先々週': today + datetime.timedelta(days=-14),
            '先週': today + datetime.timedelta(days=-7),
            '来週': today + datetime.timedelta(days=7),
            '再来週': today + datetime.timedelta(days=14),

            '次の週': today + datetime.timedelta(days=7),
            '先々週の月曜日': today + datetime.timedelta(days=-14 - weekday),
            '先々週の火曜日': today + datetime.timedelta(days=-14 - weekday + 1),
            '先々週の水曜日': today + datetime.timedelta(days=-14 - weekday + 2),
            '先々週の木曜日': today + datetime.timedelta(days=-14 - weekday + 3),
            '先々週の金曜日': today + datetime.timedelta(days=-14 - weekday + 4),
            '先々週の土曜日': today + datetime.timedelta(days=-14 - weekday + 5),
            '先々週の日曜日': today + datetime.timedelta(days=-14 - weekday + 6),
            '先週の月曜日': today + datetime.timedelta(days=-7 - weekday),
            '先週の火曜日': today + datetime.timedelta(days=-7 - weekday + 1),
            '先週の水曜日': today + datetime.timedelta(days=-7 - weekday + 2),
            '先週の木曜日': today + datetime.timedelta(days=-7 - weekday + 3),
            '先週の金曜日': today + datetime.timedelta(days=-7 - weekday + 4),
            '先週の土曜日': today + datetime.timedelta(days=-7 - weekday + 5),
            '先週の日曜日': today + datetime.timedelta(days=-7 - weekday + 6),
            '来週の月曜日': today + datetime.timedelta(days=7 - weekday),
            '来週の火曜日': today + datetime.timedelta(days=7 - weekday + 1),
            '来週の水曜日': today + datetime.timedelta(days=7 - weekday + 2),
            '来週の木曜日': today + datetime.timedelta(days=7 - weekday + 3),
            '来週の金曜日': today + datetime.timedelta(days=7 - weekday + 4),
            '来週の土曜日': today + datetime.timedelta(days=7 - weekday + 5),
            '来週の日曜日': today + datetime.timedelta(days=7 - weekday + 6),
            '再来週の月曜日': today + datetime.timedelta(days=14 - weekday),
            '再来週の火曜日': today + datetime.timedelta(days=14 - weekday + 1),
            '再来週の水曜日': today + datetime.timedelta(days=14 - weekday + 2),
            '再来週の木曜日': today + datetime.timedelta(days=14 - weekday + 3),
            '再来週の金曜日': today + datetime.timedelta(days=14 - weekday + 4),
            '再来週の土曜日': today + datetime.timedelta(days=14 - weekday + 5),
            '再来週の日曜日': today + datetime.timedelta(days=14 - weekday + 6),
            '2019-01-04': datetime.datetime(2019, 1, 4, tzinfo=tz),
            '2019-1-4': datetime.datetime(2019, 1, 4, tzinfo=tz),
            '19-01-04': datetime.datetime(2019, 1, 4, tzinfo=tz),
            '19-1-4': datetime.datetime(2019, 1, 4, tzinfo=tz),
            '1/4': datetime.datetime(today.year, 1, 4, tzinfo=tz),
            '12/8': datetime.datetime(today.year, 12, 8, tzinfo=tz),
            '99/12/13': datetime.datetime(2099, 12, 13, tzinfo=tz),
        }

        for dt_ja in date_table:
            dt, ctx = self.cal.parseDT(dt_ja, tzinfo=tz)
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            print(f'{dt_ja}:\t{dt}, {dt == date_table[dt_ja]}')
            self.assertEqual(date_table[dt_ja], dt)

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
