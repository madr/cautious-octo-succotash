import hashlib
from django import template

from core.lib import TimeUtil
from core.models import Project

register = template.Library()


@register.filter
def sumtime(progress_set):
    return sum([p.duration for p in progress_set.all()])


@register.filter
def billable(progress_set):
    all_time = sum([p.duration for p in progress_set.all()])
    billable_time = sum([p.duration for p in progress_set.filter(project__billable=True)])
    return int((billable_time / all_time) * 100)


@register.filter
def hhmm(value):
    return TimeUtil.hhmm(value)


@register.filter
def gravatar(email):
    return hashlib.md5(email.encode('latin1')).hexdigest()


@register.filter
def pretty_minutes(minutes):
    return TimeUtil.duration(TimeUtil.correct(minutes))


@register.filter
def pretty_period(year, week):
    return TimeUtil.period(year, week)


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
