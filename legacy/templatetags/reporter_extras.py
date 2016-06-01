#coding: utf-8
from datetime import datetime
import hashlib
from time import strptime
from django import template
from legacy.utils import SumUtil
from core.lib import TimeUtil

register = template.Library()

@register.filter
def hhmm(value):
    return TimeUtil.hhmm(value)

@register.filter
def gravatar(email):
    return hashlib.md5(email).hexdigest()

@register.filter
def sum(progresses):
    return SumUtil.minutes(progresses)

@register.filter
def pretty(minutes):
    return TimeUtil.duration(TimeUtil.correct(minutes))

@register.filter
def fancy(year, week):
    return TimeUtil.period(year, week)

@register.filter
def get_range(stop_value):
    return range(1, stop_value + 1)

@register.filter
def get_date(date_str):
    # TODO: flytta till TimeUtil
    datestruct = strptime(date_str, "%Y-%m-%d")
    date = datetime(datestruct[0], datestruct[1], datestruct[2])
    return date

@register.filter
def sum_col(progresses_grouped_by_project_and_date, column_id):
    column_id -= 1
    sum = 0

    for project_name, columns in progresses_grouped_by_project_and_date:
        progresses = columns[column_id][1]

        for progress in progresses:
            sum += progress["minutes"]

    return sum


@register.filter
def hours(hhmm):
    if hhmm == "00:00":
        return "-"

    hh, mm = hhmm.split(":")

    mm = mm.replace("15", "¼")
    mm = mm.replace("30", "½")
    mm = mm.replace("45", "¾")
    mm = mm.replace("00", "")

    if hh == "00":
        return mm

    return "%d%s" % (int(hh), mm)
