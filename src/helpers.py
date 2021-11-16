# Project-Management.logger - helper for logging
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import os
import logging
import time as _time

import config.config as config

class Logger:
    def __new__(cls, name: str, filename: str, writeConsole: bool = True, writeFile: bool = True):
        """Generates logging.logger with defaults set

        Args:
            name (str): specify the logger's name
            file (str): specify log file name

        Returns:
            logging.logger
        """

        formatter = logging.Formatter('%(asctime)s <%(name)s> %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)

        if writeConsole:
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(formatter)
            log.addHandler(sh)

        if writeFile and not filename is None:
            if not os.path.exists(f"{config.PATH_ROOT}/logs"):
                os.mkdir(f"{config.PATH_ROOT}/logs")
            fh = logging.FileHandler(filename=f"{config.PATH_ROOT}/logs/{filename}")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            log.addHandler(fh)

        return log

class Date:
    """ This is pulled from python datetime due to it throwing 'TypeError: 'datetime.date' object is not callable' """
    _DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    _DAYS_BEFORE_MONTH = [-1]  # -1 is a placeholder for indexing purposes.
    dbm = 0
    for dim in _DAYS_IN_MONTH[1:]:
        _DAYS_BEFORE_MONTH.append(dbm)
        dbm += dim
    del dbm, dim

    def __init__(self, year: int, month: int, day: int):
        self.year= year
        self.month = month
        self.day = day

    #def __call__(self, year: int, month: int, day: int):
    #    pass # temporary fix for a much larger issue, like this entire class

    def __str__(self):
        return "%04d-%02d-%02d" % (self.year, self.month, self.day)

    def __sub__(self, other):
        """Subtract two dates"""
        return self.toordinal() - other.toordinal()

    def toordinal(self):
        """Return proleptic Gregorian ordinal for the year, month and day.

        January 1 of year 1 is day 1.  Only the year, month and day values
        contribute to the result.
        """
        return self._ymd2ord(self.year, self.month, self.day)

    def _is_leap(self, year):
        "year -> 1 if leap year, else 0."
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def _days_in_month(self, year, month):
        "year, month -> number of days in that month in that year."
        assert 1 <= month <= 12, month
        if month == 2 and self._is_leap(year):
            return 29
        return self._DAYS_IN_MONTH[month]

    def _days_before_year(self, year):
        "year -> number of days before January 1st of year."
        y = year - 1
        return y*365 + y//4 - y//100 + y//400

    def _days_before_month(self, year, month):
        "year, month -> number of days in year preceding first day of month."
        assert 1 <= month <= 12, 'month must be in 1..12'
        return self._DAYS_BEFORE_MONTH[month] + (month > 2 and self._is_leap(year))

    def _ymd2ord(self, year, month, day):
        "year, month, day -> ordinal, considering 01-Jan-0001 as day 1."
        assert 1 <= month <= 12, 'month must be in 1..12'
        dim = self._days_in_month(year, month)
        assert 1 <= day <= dim, ('day must be in 1..%d' % dim)
        return (self._days_before_year(year) +
                self._days_before_month(year, month) +
                day)

    def Today():
        t = _time.time()
        y, m, d, hh, mm, ss, weekday, jday, dst = _time.localtime(t)
        return Date(y, m, d)

    def Set(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day
        return self