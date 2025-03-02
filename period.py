from calendar import Day
from datetime import date, timedelta


def generate(rule, start, end):
    dateiter = rule(start)
    for eventdate in dateiter:
        if eventdate < end:
            yield eventdate
        else:
            break


def years(eventdate, step=1):
    def years_rule(start):
        nonlocal eventdate, step

        # <tbd> some dates may raise ValueError, for example 29 feb
        if eventdate < start:
            y = start.year + ((step - start.year - eventdate.year) % step)
            current = eventdate.replace(year=y)
        else:
            current = eventdate

        while True:
            yield current
            current = current.replace(year=current.year + step)

    return years_rule


def months(monthday=1, step=1):
    def pick_date(y, m):
        nonlocal monthday
        try:
            result = date(y, m, monthday)
        except ValueError:
            m = m + 1 if m < 12 else 1
            result = date(y, m, 1) - timedelta(days=1)

        return result

    def months_rule(start):
        nonlocal step

        current = start
        y = current.year
        m = current.month

        while True:
            yield pick_date(y, m)
            m += step
            if m > 12:
                m %= 12
                y += 1

    return months_rule


def weeks(weekday, step=1):
    def weeks_rule(start):
        nonlocal weekday
        nonlocal step

        skipdays = (7 - start.weekday() + weekday) % 7
        current = start + timedelta(days=skipdays)
        while True:
            yield current
            current += timedelta(days=7 * step)

    return weeks_rule


def _is_weekend(day):
    return (day == Day.SATURDAY) or (day == Day.SUNDAY)


def workdays():
    def workdays_rule(start):
        current = start
        if _is_weekend(weekday := start.weekday()):
            current += timedelta(days=(7 - weekday))

        deltaday = timedelta(days=1)
        deltaweekend = timedelta(days=3)
        while True:
            yield current
            if current.weekday() == Day.FRIDAY:
                current += deltaweekend
            else:
                current += deltaday

    return workdays_rule


def weekends():
    def weekends_rule(start):
        current = start
        deltaworkdays = timedelta(days=6)
        if not _is_weekend(weekday := start.weekday()):
            current += timedelta(days=(5 - weekday))
        elif weekday == Day.SUNDAY:
            yield current
            current += deltaworkdays

        deltaday = timedelta(days=1)
        while True:
            yield current
            yield (current := current + deltaday)
            current += deltaworkdays

    return weekends_rule


def single(eventdate):
    def single_rule(start):
        nonlocal eventdate

        if eventdate >= start:
            yield eventdate

    return single_rule
