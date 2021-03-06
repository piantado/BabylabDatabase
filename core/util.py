from __future__ import division

import datetime
import dateutil.relativedelta


def calc_age(dob):
    dt1 = datetime.datetime(dob.year, dob.month, dob.day)
    dt2 = datetime.datetime.now()
    rd = dateutil.relativedelta.relativedelta(dt2, dt1)
    return "%d years, %d months, %d days" % (rd.years, rd.months, rd.days)

def calc_age_dec(dob):
    dt1 = datetime.datetime(dob.year, dob.month, dob.day)
    dt2 = datetime.datetime.now()
    rd = dateutil.relativedelta.relativedelta(dt2, dt1)
    return round(rd.years + (rd.months/12) + (rd.days/365), 2)

def calc_age_months(dob):
    dt1 = datetime.datetime(dob.year, dob.month, dob.day)
    dt2 = datetime.datetime.now()
    rd = dateutil.relativedelta.relativedelta(dt2, dt1)
    #averaging months to be 30 days long
    return round(rd.years*12 + (rd.months) + (rd.days/30), 2)