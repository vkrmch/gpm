import datetime
import time
import pytest
from gpm import formatting


time_in_seconds = [
    10,
    30,
    35,
    121,
    5000,
    90005,
    3456500
]

time_formatted = [
    '10.0s',
    '30.0s',
    '35.0s',
    '2m 1.0s',
    '1h 23m 20.0s',
    '1days 1h 5.0s',
    '40days 8m 20.0s'
]


sizes = [
    10,
    100,
    1000,
    10000,
    100000,
    1000000,
    10000000
]

sizes_kb = []
for size in sizes:
    sizes_kb.append(size / 1024)

sizes_formatted = [
    '10.00b',
    '100.00b',
    '1000.00b',
    '9.77kb',
    '97.66kb',
    '976.56kb',
    '9.54mb'
]

sizes_formatted_mb = [
    '0.00mb',
    '0.00mb',
    '0.00mb',
    '0.01mb',
    '0.10mb',
    '0.95mb',
    '9.54mb'
]


def test_decimal_round():
    assert formatting.decimal_round(5.6666, 3) == '5.667'


def test_str_trim_double_quotes():
    assert formatting.str_trim_double_quotes('"test_str"') == 'test_str'


def test_str_strip_chars():
    invalid_chars = [' ', '*']
    invalid_str = 't*h*i s'
    valid_str = 'this'
    assert formatting.str_strip_chars(invalid_str, *invalid_chars) == valid_str


# Time specific


def test_formatting():
    output = []
    for time in time_in_seconds:
        output.append(formatting.time_pretty(time))

    assert time_formatted == output


def test_time_invalid_format():
    with pytest.raises(Exception):
        formatting.time_now('invalid_format')


def test_time_specific_invalid_format():
    with pytest.raises(Exception):
        formatting.time_specific(time.time(), ts_format='invalid_format')


def test_time_no_format():
    now_str_from_formatting = formatting.time_now()
    valid = False
    if now_str_from_formatting != '':
        valid = True

    assert valid


def test_time_specific_no_format():
    now_str_from_formatting = formatting.time_specific(time.time())
    valid = False
    if now_str_from_formatting != '':
        valid = True

    assert valid


def test_time_valid_format():
    now = datetime.datetime.now()
    now_str = now.strftime('%Y%m%d%H')

    now_str_from_formatting = formatting.time_now('YYYYMMDDHH')
    assert now_str == now_str_from_formatting


def test_time_specific_valid_format():
    now = time.time()
    now_str = datetime.datetime.fromtimestamp(now).strftime('%Y%m%d%H')
    now_str_from_formatting = formatting.time_specific(now, 'YYYYMMDDHH')

    assert now_str == now_str_from_formatting


# File Size


def test_size_only_no_unit():
    # this should return same output as input
    output = []
    for size in sizes:
        output.append(formatting.fsize_pretty(size, return_size_only=True))

    assert sizes == output


def test_size_only_with_valid_unit():
    output = []
    for size in sizes:
        output.append(formatting.fsize_pretty(size, return_size_only=True, unit='kb'))

    assert sizes_kb == output


def test_size_no_unit():
    output = []
    for size in sizes:
        output.append(formatting.fsize_pretty(size))

    assert sizes_formatted == output


def test_size_specific_unit():
    output = []
    for size in sizes:
        output.append(formatting.fsize_pretty(size, unit='mb'))

    assert sizes_formatted_mb == output


def test_invalid_unit():
    with pytest.raises(Exception):
        formatting.fsize_pretty(10, unit='invalid')


def test_size_very_large_size():
    assert formatting.fsize_pretty(1024 ** 6)


# Temperature

def test_temp_pretty_default():
    assert formatting.temperature_pretty(52.56) == "53" + '\u00b0' + "F"


def test_temp_pretty_with_unit():
    assert formatting.temperature_pretty(52.56, unit='C') == "53" + '\u00b0' + "C"


def test_temp_pretty_without_rounding():
    assert formatting.temperature_pretty(52.56, round_off=False) == "52.56" + '\u00b0' + "F"


def test_temp_pretty_invalid_unit():
    assert formatting.temperature_pretty(52.56, unit='X') == "53" + '\u00b0' + "F"

