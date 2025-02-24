from calendar import Day
from datetime import date

import period
from cashflow import Cashflow, basic_printer


if __name__ == "__main__":
    cf = Cashflow()

    # set timeframe
    cf.set_range(start=date(2025, 1, 1), end=date(2026, 1, 1))

    # rent
    cf.add(period.months(), 1200)
    # subscription
    cf.add(period.months(), 15)
    # groceries
    cf.add(period.weeks(Day.SATURDAY), 100)
    # lunch
    cf.add(period.workdays(), 10)
    # haircut
    cf.add(period.weeks(Day.SUNDAY, 4), 35)

    # generate "report"
    flows = cf.produce()
    basic_printer(flows)
