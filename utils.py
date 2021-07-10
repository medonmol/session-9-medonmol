from time import perf_counter
from functools import wraps
from dateutil.relativedelta import relativedelta
from datetime import date
from numpy.random import randint
from numpy import float64, int32


class CustomException(Exception):

    """
    Custom Exception class
    """

    def __init__(self, message):
        self.messaege = message

    def __repr__(self):
        return self.message


def timer(n):
    """
    Decorates a function and retuns the avg runtime over n runs
    """

    def timer_outer(fn):
        @wraps(fn)
        def timer_inner(*args, **kwargs):
            total = 0
            for _ in range(n):
                start = perf_counter()
                out = fn(*args, **kwargs)
                total += perf_counter() - start
            print(
                f"{fn.__name__} runtime averaged over {n} iterations : {total * 1.0 / n} seconds"
            )
            return out

        return timer_inner

    return timer_outer


def get_age(x):
    """
    function to calculate the age of a profile
    """
    if isinstance(x, dict):
        age = relativedelta(date.today(), x.get("birthdate"))
    else:
        age = relativedelta(date.today(), x.birthdate)
    age = age.years + age.months // 12.0 + age.days / 365.0
    return age


def get_coord(x):
    """
    function to calculate the x and y coordinate of a profile in float
    """
    coord = dict()
    if isinstance(x, dict):
        coord["x_coord"] = float(x.get("current_location")[0])
        coord["y_coord"] = float(x.get("current_location")[1])
    else:
        coord["x_coord"] = float(x.current_location[0])
        coord["y_coord"] = float(x.current_location[1])
    return coord


def generate_random_price():
    """
    Generates a random price series
    """
    price = []
    x = randint(50, 5000)
    for _ in range(50):
        rand_int = randint(981, 1020) / 1000.0
        x *= rand_int
        price.append(round(x))
    return price


def validate_stock_datatype(fn):
    """
    Decorator to perform basic data validation on the calculate_stock_market_value function
    """

    def inner(*args, **kwargs):
        data = kwargs["data"] if "data" in kwargs else args[0]
        data = [data] if not isinstance(data, list) else data
        for tup in data:
            if not isinstance(tup, tuple):
                raise CustomException(
                    "Please send the stock market data as a namedtuple"
                )

            if not (
                isinstance(tup.name, str)
                and isinstance(tup.symbol, str)
                and isinstance(tup.price, list)
                and isinstance(tup.open, (int, float, int32, float64))
                and isinstance(tup.high, (int, float, int32, float64))
                and isinstance(tup.close, (int, float, int32, float64))
                and isinstance(tup.weight, (float, float64))
            ):

                raise CustomException(f"incorrect datatype in namedtuple {tup}")
        return fn(*args, **kwargs)

    return inner
