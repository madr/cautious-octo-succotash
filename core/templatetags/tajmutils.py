import datetime
import hashlib

from django import template
from django.utils.translation import ugettext

from core.lib import TimeUtil

register = template.Library()


@register.filter
def sumtime(progress_set, **kwargs):
    if isinstance(progress_set, list):
        return sum([p.duration for p in progress_set])
    if kwargs:
        return sum([p.duration for p in progress_set.filter(**kwargs)])
    return sum([p.duration for p in progress_set.all()])


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def times(value, arg):
    return int(value) * int(arg)


@register.filter
def billable(progress_set, days=0):
    before = datetime.datetime.today() - datetime.timedelta(days=days)
    all_time = sum([p.duration for p in progress_set.filter(done_at__lte=before)])
    billable_time = sum([p.duration for p in progress_set.filter(project__billable=True, done_at__lte=before)])

    try:
        billable = int((billable_time / all_time) * 100)
    except ZeroDivisionError:
        billable = 0

    return billable


@register.filter
def hhmm(value):
    return TimeUtil.hhmm(value)


@register.filter
def gravatar(email):
    return hashlib.md5(email.encode('latin1')).hexdigest()


@register.filter
def pretty_minutes(minutes):
    ''' transform a duration (in minutes) to spoken time '''
    if minutes == 0:
        return ugettext("ingen")

    hh = (minutes - (minutes % 60)) / 60
    mm = minutes % 60
    hh_label = ugettext("timmar")

    if hh == 1:
        hh_label = ugettext("timme")

    if hh == 0:
        return "%d %s" % (mm, ugettext("minuter"))

    if mm == 0:
        return "%d %s" % (hh, hh_label)

    ret = "%d %s, %d %s" % (hh, hh_label, mm, ugettext("minuter"))

    return ret


@register.filter
def pretty_period(year, week):
    return TimeUtil.period(year, week)


@register.filter
def hours(hhmm):
    if hhmm == '00:00' or hhmm == '0:00':
        return '-'

    hh, mm = hhmm.split(':')

    mm = mm.replace('15', '¼')
    mm = mm.replace('30', '½')
    mm = mm.replace('45', '¾')
    mm = mm.replace('00', '')

    if hh == '00' or hh == '0':
        return mm

    if mm == '':
        return int(hh)

    return '%d%s' % (int(hh), mm)
