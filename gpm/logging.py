"""
Provides ability to log output into a file or to console

The log files reside in a folder called "log" in the directory 
where Python script is 

Python script:
folderX/ScriptY.py

log file:
folderX/log/ScriptY/ScriptY<xxxx>.log
"""
import re
import logging
import logging.handlers
import os
from gpm import config, formatting

# Read config
c = config.Config(script=__file__, create=True)
c.read()


# Define log class
class Log(object):
    def __init__(self, script=None, tsformat=None, keyword=None, log_level=None, logger_name=None, rotating=False,
                 console=True, log_entry_format_separator=None):

        # Define logger
        logger = get_logger(logger_name)
        logger.setLevel(log_level)

        if tsformat is None:
            tsformat = c.log_file_default_tsformat

        if log_level is None:
            log_level = c.log_level

        if log_entry_format_separator is None:
            log_entry_format_separator = c.log_entry_format_separator

        # Define log format
        c.log_entry_format = c.log_entry_format.format(separator=log_entry_format_separator)
        formatter = logging.Formatter(c.log_entry_format, datefmt=c.log_date_format)

        # Check if handlers are already added. If not add them
        # This avoids duplicate messages
        if not logger.handlers:
            # Log to Console by default unless otherwise defined to not
            if console:
                console = logging.StreamHandler()
                console.setLevel(log_level)
                console.setFormatter(formatter)
                logger.addHandler(console)

            # If Script specified then also do file based
            if script is not None:
                ts = '_' + formatting.time_now(tsformat)

                # Extract Script ID which is equal to ScriptY for ScriptY.py
                script_id = os.path.splitext(os.path.basename(script))[0]

                # Define log dir
                log_dir = os.path.join(os.path.dirname(os.path.abspath(script)), 'log', script_id)

                # Check if the folder exists and create if necessary
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)

                # This optional keyword gets appended to the file name
                # after the timestamp
                if keyword:
                    # Strip characters that OS won't allow
                    keyword = re.sub('[/\:?"|*]', '', keyword)
                    keyword = '_' + keyword
                else:
                    keyword = ''

                if rotating:
                    # Difference in the name is that there will be no
                    # timestamp for rotating logs
                    log_file = script_id + keyword + '.log'
                    log_file_path = os.path.join(log_dir, log_file)
                    file = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=c.log_maxbytes,
                                                                backupCount=c.log_backupcount)
                else:
                    log_file = script_id + ts + keyword + '.log'
                    log_file_path = os.path.join(log_dir, log_file)
                    file = logging.FileHandler(log_file_path)

                file.setLevel(log_level)
                file.setFormatter(formatter)
                logger.addHandler(file)

                # Assign path variables
                self._log_dir = log_dir
                self._log_file = log_file
                self._log_file_path = log_file_path

        # Assign logger values to self and global log object
        self._logger = logger

    def start(self):
        self._logger.info(c.log_msg_begin)

    def end(self):
        self._logger.info(c.log_msg_end)
        logging.shutdown()

        # Remove handlers
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)

    def info(self, text):
        self._logger.info(text)

    def error(self, text):
        self._logger.error(text)

    def debug(self, text):
        self._logger.debug(text)

    def warning(self, text):
        self._logger.warning(text)

    def critical(self, text):
        self._logger.critical(text)


def get_logger(logger_name):
    if logger_name is None:
        logger_name = 'main'
    elif logger_name == '__main__':
        logger_name = 'main'
    else:
        logger_name = 'main.' + logger_name

    return logging.getLogger(logger_name)
