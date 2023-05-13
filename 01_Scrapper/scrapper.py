"""Space to use scrapper function
    """

import datetime as dt
import scrapper_function

scrapper_function.forex_factory_scrapper(
    start_date = dt.datetime(year=2022, month=1, day=3),
    end_date = dt.datetime(year=2023, month=5, day=13)
)
