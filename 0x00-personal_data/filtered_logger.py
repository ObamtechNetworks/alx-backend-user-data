#!/usr/bin/env python3
"""Contains a function that returns the log message obfuscated"""

import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """A function that returns a log message obfuscated

    Args:
        fields (List[str]): A list of strings representing fields to obfuscate
        redaction (str): a string representing by
        what the field will be obfuscated
        message (str): a strin representing the log line
        separator (str): a string representing by which
        character is separating all fields in the log line (message)
        Returns:
            Returns the log message obfuscated
    """
    pattern = '|'.join(f'{field}=[^{separator}]+' for field in fields)
    return re.sub(pattern,
                  lambda m: m.group(0).split('=')[0] + '=' + redaction,
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Class constructor initializer,
        accepts a list of strings

        Args:
            fields (List[str]): A list of strings
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and redact sensitive fields.
        """
        # Get the original log message
        original_message = record.getMessage()
        # Obfuscate sensitive fields in the log message
        filtered_message = filter_datum(self.fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        # Replace the original message in the log
        # record with the filtered message
        record.msg = filtered_message
        # Use the parent class to format the log record
        return super(RedactingFormatter, self).format(record)
