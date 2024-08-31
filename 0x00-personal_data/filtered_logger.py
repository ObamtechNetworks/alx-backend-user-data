#!/usr/bin/env python3
"""Contains a function that returns the log message obfuscated"""

import re
from typing import List


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
