import random
import re
import string

from re import Pattern
from typing import List

ALPHA_NUM_REGEX: Pattern = re.compile(r'[A-Za-z0-9]+')


def sanitize_text(text: str) -> str:
    """ Remove symbols from given argument `text`.
            e.g. "wow 123_ @#$%    1" --> "wow_123_1"

    Args:
        text (str): Text to remove symbols from.

    Returns:
        str: Sanitized text.
    """

    words: List[str] = ALPHA_NUM_REGEX.findall(text.lower())
    return "_".join(words)


def get_random_string(string_length: int = 6) -> str:
    """ Generate string of random alpha-numeric charcters of a given length `string_length`.

    Args:
        string_length (int, default = 6): String length of returned string.

    Returns:
        str: Random string containing alpha-numeric characters.
    """

    options: str = string.ascii_letters + string.digits
    random_chars: List[str] = random.choices(options, k=string_length)
    return "".join(random_chars)
