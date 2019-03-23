import os
import shutil
import pytest
from gpm import logging


messages = {
    'info': 'this is info message',
    'error': 'this is error message',
    'debug': 'this is debug message',
    'warning': 'this is warning message',
    'critical': 'this is critical message'
}


def remove_log_folder(folder=None):
    if folder is None:
        folder = os.path.join(os.path.dirname(__file__), 'log')

    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)


def print_messages(log):
    log.start()
    for key, value in messages.items():
        getattr(log, key)(value)
    log.end()


def test_console():
    log = logging.Log()
    print_messages(log)

    # Check for existence of log file; no log file should exist
    with pytest.raises(Exception):
        a = log['_log_file_path']


def test_file_no_tsformat():
    remove_log_folder()
    log = logging.Log(__file__)
    print_messages(log)
    assert log._log_file_path
    remove_log_folder()


def test_file_tsformat():
    remove_log_folder()
    log = logging.Log(__file__, tsformat='YYYYMMDD')
    print_messages(log)
    assert log._log_file_path
    remove_log_folder()


def test_file_tsformat_keyword():
    remove_log_folder()
    log = logging.Log(__file__, tsformat='YYYYMMDD', keyword='test/')
    print_messages(log)
    assert log._log_file_path
    remove_log_folder()


def test_log_level():
    remove_log_folder()
    # This test will suppress Debug messages
    log = logging.Log(log_level=20)
    print_messages(log)

    # Check existence of log files - nothing should exists since it's console only
    with pytest.raises(Exception):
        a = log['_log_file_path']

    remove_log_folder()


def test_rotating():
    remove_log_folder()
    log = logging.Log(__file__, rotating=True, console=False)

    log.start()
    for i in range(0, 40000):
        log.info(i)
    log.end()

    # find the directory listing
    files = os.listdir(log._log_dir)
    valid = False
    if len(files) > 1:
        valid = True

    assert valid
    remove_log_folder()






