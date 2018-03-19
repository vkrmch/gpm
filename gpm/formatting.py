"""
 Useful formatting functions for Time, Decimal, File Sizes, Strings, Temperature
"""
import datetime
from operator import itemgetter
from gpm import config

# Read config
c = config.Config(script=__file__, create=True)
c.read()


def time_now(ts_format=None):
    if ts_format is None:
        ts_format="YYYYMMDDHHMISS"
    return datetime.datetime.now().strftime(c.ts_formats.get(ts_format))


def time_specific(ts, ts_format=None):
    if ts_format is None:
        ts_format="YYYYMMDDHHMISS"
    return datetime.datetime.fromtimestamp(int(ts)).strftime(
        c.ts_formats.get(ts_format))


def fsize_pretty(size_in_bytes, return_size_only=False, unit=None):
    conversion = {
        'b': size_in_bytes,
        'kb': size_in_bytes/1024,
        'mb': size_in_bytes/(1024**2),
        'gb': size_in_bytes/(1024**3),
        'tb': size_in_bytes/(1024**4)
    }

    if return_size_only:
        if not unit:
            unit = 'b'
        return conversion[unit]
    else:
        if not unit:
            # Sort by ascending order of value to pick the first >1 value
            for size_key, size in sorted(conversion.items(), key=itemgetter(1)):
                if size > 1:
                    return decimal_round(size, 2) + size_key
        else:
            return decimal_round(conversion[unit], 2) + unit


def time_pretty(time_in_seconds):
    if time_in_seconds is None:
        time_in_seconds = 0
    if time_in_seconds < 60:
        return decimal_round(time_in_seconds, 1) + 's'
    elif time_in_seconds < (60**2):
        minutes = time_in_seconds/60
        minutes_int = int(minutes)
        return str(minutes_int) + 'm ' + time_pretty(time_in_seconds -
                                                     minutes_int*60)
    elif time_in_seconds < ((60**2)*24):
        hours = time_in_seconds/(60**2)
        hours_int = int(hours)
        return str(hours_int) + 'h ' + time_pretty(time_in_seconds -
                                                   hours_int*(60**2))
    else:
        days = time_in_seconds/((60**2)*24)
        days_int = int(days)
        return str(days_int) + 'days ' + time_pretty(time_in_seconds -
                                                     days_int*(60**2)*24)


def decimal_round(num, factor=2):
    format_string = '{:.' + str(factor) + 'f}'
    return format_string.format(num)


def str_trim_double_quotes(input_str):
    if input_str.startswith('"') and input_str.endswith('"'):
        return input_str[1:-1]


def str_strip_chars(input_str, *args):
    for arg in args:
        input_str = input_str.replace(arg, '')
    return input_str


def temperature_pretty(temperature, round_off=True, unit='F'):
    if round_off:
        temperature = decimal_round(temperature, 0)

    if not unit:
        unit = 'F'

    if not (unit in ['C', 'F']):
        unit = 'F'

    return str(temperature) + '\u00b0' + unit
