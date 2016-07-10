import hashlib
from django import template

from core.lib import TimeUtil

register = template.Library()

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
