import random
import re
import string


class Utils:

    @classmethod
    def remove_symbols(self, text: str) -> str:
        """ Remove symbols from given `text` argument.
            e.g. "wow 123_ @#$%    1" --> "wow_123_1"

        Args:
            text (str): Text to remove symbols from.

        Returns:
            str: Sanitized text.
        """

        return "_".join(map(str.strip, re.findall(r'[A-Za-z0-9]+', text.lower())))

    @classmethod
    def get_random_string(self, string_length: int = 6) -> str:
        """ Generate string of random alpha-numeric charcters of a given length `string_length`.

        Args:
            string_length (int, default = 6): String length of returned string.

        Returns:
            str: Random string containing alpha-numeric characters.
        """

        options = string.ascii_letters + string.digits
        return "".join(random.choices(options, k=string_length))
