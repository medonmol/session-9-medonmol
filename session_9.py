from faker import Faker
from collections import namedtuple
from utils import (
    timer,
    get_age,
    get_coord,
    generate_random_price,
    CustomException,
    validate_stock_datatype,
)
from numpy import mean, max, unique, argmax, sum
from numpy.random import uniform


class GenerateProfiles:
    """
    Generates profiles using the faker library
    """

    def __init__(self, n=10000):
        self.fake = Faker()
        self.profiles = []
        self.num = n
        self.profile = namedtuple("Profile", self.fake.profile().keys())
        self.profile.__doc__ = (
            "A NamedTuple containing fake profiles generated using Faker"
        )
        for _ in range(self.num):
            self.profiles.append(self.fake.profile())

    def get_profiles_dict(self):
        "Returns the generated profiles as a list of dictionary"
        return self.profiles

    def get_profiles_tup(self):
        """
        Returns the generated profiles as a list of namedtuples
        """
        return [self.profile(**x) for x in self.profiles]


@timer(10)
def calculate_stats_namedtuple_timed(list_named_tuple):
    """
    Wrapper method around calculate_stats_namedtuple method,
    retuns the result as well as the runtime of the function
    averaged over 10 runs
    """
    return calculate_stats_namedtuple(list_named_tuple)


def calculate_stats_namedtuple(list_named_tuple):
    """
    Accepts a list of namedtuples and calculates
    the largest blood type, mean current location and
    average age
    """
    blood_group = [x.blood_group for x in list_named_tuple]
    age = [get_age(x) for x in list_named_tuple]
    coord = [get_coord(x) for x in list_named_tuple]

    avg_coord_x = round(mean([x["x_coord"] for x in coord]), 2)
    avg_coord_y = round(mean([x["y_coord"] for x in coord]), 2)

    blood_type, count = unique(blood_group, return_counts=True)
    largest_blood_type = blood_type[argmax(count)]

    oldest_age = round(max(age), 2)
    average_age = round(mean(age), 2)

    output = namedtuple(
        "Output",
        "largest_blood_type, oldest_age, average_age, mean_current_location_x, mean_current_location_y",
    )
    output.__doc__ = """Contains the largest blood type, the oldest age of a person in the profiles, mean x and y coordinates of all the candidates in the profiles."""
    output.largest_blood_type.__doc__ = (
        "The most common blood type in the generated profiles."
    )
    output.oldest_age.__doc__ = "Age of the oldest person in the generated profiles."
    output.average_age.__doc__ = "Average age of the people in the generated profiles."
    output.mean_current_location_x.__doc__ = (
        "Mean x coordinate of all the people in the generated profiles."
    )
    output.mean_current_location_y.__doc__ = (
        "Mean y coordinate of all the people in the generated profiles"
    )
    return output(largest_blood_type, oldest_age, average_age, avg_coord_x, avg_coord_y)


@timer(10)
def calculate_stats_dict_timed(list_named_tuple):
    """
    Wrapper method around calculate_stats_dict method,
    retuns the result as well as the runtime of the function
    averaged over 10 runs
    """
    return calculate_stats_dict(list_named_tuple)


def calculate_stats_dict(profile_dict):
    """
    Accepts a list of dictionaries and calculates
    the largest blood type, mean current location and
    average age
    """
    blood_group = [x.get("blood_group") for x in profile_dict]
    age = [get_age(x) for x in profile_dict]
    coord = [get_coord(x) for x in profile_dict]

    avg_coord_x = round(mean([x["x_coord"] for x in coord]), 2)
    avg_coord_y = round(mean([x["y_coord"] for x in coord]), 2)

    blood_type, count = unique(blood_group, return_counts=True)
    largest_blood_type = blood_type[argmax(count)]
    oldest_age = round(max(age), 2)
    average_age = round(mean(age), 2)

    return {
        "largest_blood_type": largest_blood_type,
        "oldest_age": oldest_age,
        "average_age": average_age,
        "mean_current_location_x": avg_coord_x,
        "mean_current_location_y": avg_coord_y,
    }


def generate_fake_data_stock_market():
    """
    Generates fake stock market data.

    """
    fake = Faker()
    all_companies = []
    company_name = [fake.company() for _ in range(100)]
    stock_name = ["".join([x for x in st if x.isupper()]) for st in company_name]
    tmp = uniform(1, 100, 100)
    company_weights = tmp / sum(tmp)
    company_weights = [round(x, 4) for x in company_weights]
    Stocks = namedtuple("Stocks", "name symbol price open high close weight")
    Stocks.__doc__ = "Tuple to hold the OHC and intraday price data for a given stock"
    Stocks.name.__doc__ = "Name of the Stock"
    Stocks.symbol.__doc__ = "Symbol of the Stock"
    Stocks.price.__doc__ = "List of intraday price of the Stock"
    Stocks.open.__doc__ = "Opening Price of the Stock"
    Stocks.high.__doc__ = "Highest Price of the Stock"
    Stocks.close.__doc__ = "Closing Price of the Stock"
    Stocks.weight.__doc__ = "Weight of the Stock"
    for i in range(100):
        _price = generate_random_price()
        all_companies.append(
            Stocks(
                company_name[i],
                stock_name[i],
                _price,
                _price[0],
                max(_price),
                _price[-1],
                company_weights[i],
            )
        )
    return all_companies


@validate_stock_datatype
def calculate_stock_market_value(data, weights=None):
    """
    Given a list of namedtuples containing stock market
    data, returns the stock market value for the day.
    The number of stocks is hard coded at 100, and the number of
    price readings in a day is hard coded at 50.
    """
    stock_market_value = []

    if weights is not None and len(weights) != len(data):
        raise CustomException(
            "The length of weight and all_companies arrays should be the same"
        )
    if weights is not None and sum(weights) != 1:
        raise CustomException("The sum of weights is not equal to 1")
    for j in range(50):
        stock_market_val = 0
        for i in range(len(data)):
            if weights is None:
                stock_market_val += data[i].price[j] * data[i].weight
            else:
                stock_market_val += data[i].price[j] * weights[i]
        stock_market_value.append(stock_market_val)

    # stock_market_value = price_matrix @ company_weights

    starting_smv = stock_market_value[0]
    highest_smv = max(stock_market_value)
    closing_smv = stock_market_value[-1]
    stock_market_value = namedtuple(
        "StockMarketValue", "OpeningValue,HighestValue,ClosingValue"
    )
    stock_market_value.__doc__ = (
        "Contains the opening, highest and closing value of the stock market for a day"
    )
    stock_market_value.OpeningValue.__doc__ = "Opening value of the stock market"
    stock_market_value.HighestValue.__doc__ = "Highest value of the stock market"
    stock_market_value.ClosingValue.__doc__ = "Closing value of the stock market"

    return stock_market_value(starting_smv, highest_smv, closing_smv)
