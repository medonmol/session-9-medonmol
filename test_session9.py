from collections import namedtuple
from utils import CustomException
import session_9
import pytest
from numpy import mean
from numpy.random import choice
from re import search
from time import perf_counter


@pytest.fixture(scope="session")
def get_profiles():
    profiles = session_9.GenerateProfiles(n=10000)
    return profiles


@pytest.fixture(scope="session")
def namedtuple_(get_profiles):
    return get_profiles.get_profiles_tup()


@pytest.fixture(scope="session")
def dict_(get_profiles):
    return get_profiles.get_profiles_dict()


@pytest.fixture(scope="session")
def stats_namedtuple(namedtuple_):
    return session_9.calculate_stats_namedtuple(namedtuple_)


@pytest.fixture(scope="session")
def stats_dict(dict_):
    return session_9.calculate_stats_dict(dict_)


@pytest.fixture(scope="session")
def get_fake_stock_data():
    return session_9.generate_fake_data_stock_market()


# 1
def test_generated_profiles_nt(namedtuple_):
    assert isinstance(namedtuple_[0], tuple)


# 2
def test_generated_profiles_dict(dict_):
    assert isinstance(dict_[0], dict)


# 3
def test_generated_profiles_nt_dict_equal(namedtuple_, dict_):
    for idx in choice(10000, 50, replace=False):
        assert namedtuple_[idx]._asdict() == dict_[idx]


# 4
def test_generated_profile_docstring(namedtuple_):
    assert namedtuple_[0].__doc__ is not None


# 5 check the number of profiles
def test_generated_profile_total_records_nt(namedtuple_):
    assert len(namedtuple_) == 10000


# 6
def test_generated_profile_total_records_dict(dict_):
    assert len(dict_) == 10000


# 7 Assert that the oldest age is greater than equal to average_age for namedtuple
def test_nt_result_sanity_check(stats_namedtuple):
    assert stats_namedtuple.oldest_age >= stats_namedtuple.average_age


# 8 Assert that the oldest age is greater than equal to average_age for dictionary
def test_dict_result_sanity_check(stats_dict):
    assert stats_dict["oldest_age"] >= stats_dict["average_age"]


# 9 Assert that the results from namedtuple and dictionary are the same
def test_generated_results_nt_dict_equal(stats_namedtuple, stats_dict):
    assert stats_namedtuple._asdict() == stats_dict


# 10 Assert that the namedtuple is faster than dictionary


def test_time_function(namedtuple_, dict_):
    tuple_time = []
    dict_time = []
    for _ in range(10):
        start = perf_counter()
        _ = session_9.calculate_stats_namedtuple(namedtuple_)
        tuple_time.append(perf_counter() - start)
        start_ = perf_counter()
        _ = session_9.calculate_stats_dict(dict_)
        dict_time.append(perf_counter() - start_)

    assert mean(tuple_time) < mean(dict_time)


# 11


def test_stock_check_data(get_fake_stock_data):
    assert len(get_fake_stock_data) == 100


# 12


def test_stock_check_nt_doctring(get_fake_stock_data):
    assert search("stock", get_fake_stock_data[0].__doc__)


# 13


def test_stock_check_price_max(get_fake_stock_data):
    assert max(get_fake_stock_data[0].price) == get_fake_stock_data[0].high


# 14
def test_stock_check_price_low(get_fake_stock_data):
    idx = choice(100, 1)[0]
    assert get_fake_stock_data[idx].price[0] == get_fake_stock_data[idx].open


# 15
def test_stock_check_incorrect_weight_input(get_fake_stock_data):
    with pytest.raises(
        CustomException,
        match="The length of weight and all_companies arrays should be the same",
    ):
        _ = session_9.calculate_stock_market_value(get_fake_stock_data, weights=[])


# 16
def test_stock_check_calculation_wrong_input_dtype():
    data = [dict()]
    with pytest.raises(
        CustomException, match="Please send the stock market data as a namedtuple"
    ):
        _ = session_9.calculate_stock_market_value(data)


# 17


def test_stock_check_wrong_input_data_value():
    tmp = namedtuple("Stocks", "name symbol price open high close weight")
    data = tmp("TESLA", "TSLA", [10000, 110000], 10000, "110000", 110000, 0.5)
    with pytest.raises(CustomException, match="incorrect datatype in *."):
        _ = session_9.calculate_stock_market_value(data)


# 18


def test_stock_check_manual_data():
    tmp = namedtuple("Stocks", "name symbol price open high close weight")
    data = [
        tmp("TESLA", "TSLA", [100] * 50, 100, 100, 100, 0.5),
        tmp("Microsoft", "MSFT", [50] * 50, 50, 50, 50, 0.5),
    ]

    output = session_9.calculate_stock_market_value(data, weights=[0.5, 0.5])

    assert output.OpeningValue == 75
    assert output.ClosingValue == 75
    assert output.HighestValue == 75


# 19


def test_stock_check_manual_data2():
    tmp = namedtuple("Stocks", "name symbol price open high close weight")
    data = [
        tmp("TESLA", "TSLA", [100] * 50, 100, 100, 100, 0.5),
        tmp("Microsoft", "MSFT", [50] * 50, 50, 50, 50, 0.5),
    ]

    output = session_9.calculate_stock_market_value(data, weights=[0, 1])

    assert output.OpeningValue == 50
    assert output.ClosingValue == 50
    assert output.HighestValue == 50


def test_stock_check_manual_data3():
    tmp = namedtuple("Stocks", "name symbol price open high close weight")
    data = [
        tmp("TESLA", "TSLA", [100] * 50, 100, 100, 100, 0.5),
        tmp("Microsoft", "MSFT", [50] * 50, 50, 50, 50, 0.5),
    ]

    with pytest.raises(CustomException, match="The sum of weights is not equal to 1"):
        _ = session_9.calculate_stock_market_value(data, weights=[1, 1])
