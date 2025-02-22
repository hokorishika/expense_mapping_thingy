from calendar import month_abbr

from period import generate


def _cashwrap(dateiter, amount):
    # amount can be function of date or constant
    if callable(amount):
        for d in dateiter:
            yield (d, amount(d))
    else:
        for d in dateiter:
            yield (d, amount)


def basic_printer(cashflows):
    # prepare summary
    data = dict()
    for cashflow in cashflows:
        for date, amount in cashflow:
            # bin cashflows into year/month as we go through dates
            try:
                year = data[date.year]
            except KeyError:  # next year
                data[date.year] = {date.month:amount}
                continue
            try:
                year[date.month] += amount
            except KeyError:  # next month
                year[date.month] = amount

    for year, months in data.items():
        print(f"YEAR {year:04d}", end="")
        i = 0
        for month, total in months.items():
            if i % 4 == 0:
                print("\n  ", end="")
            else:
                print(" | ", end="")
            print(f"{month_abbr[month]} {total:6d}", end="")
            i += 1
        print()


class Cashflow:
    def __init__(self):
        self.flows = list()

    def add(self, rule, amount):
        self.flows.append((rule, amount))  # <todo> sort out names later

    def set_range(self, start, end):
        self.start = start
        self.end = end

    def _build(self, rule, amount):
        dates = generate(rule, self.start, self.end)
        return _cashwrap(dates, amount)

    def produce(self):
        return (self._build(*flow) for flow in self.flows)
