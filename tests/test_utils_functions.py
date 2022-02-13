import string
import unittest

from wktplot.utils import Utils


class UtilsTests(unittest.TestCase):

    def test__remove_symbols__verify_return_values(self):
        """ Verify `remove_symbols` returns expected output.
        """

        i_o = [
            ("hello", "hello"),
            ("hello 123", "hello_123"),
            ("wowzers . 456789", "wowzers_456789"),
            ("123 yep ok", "123_yep_ok"),
            ("okeey !@#$%^&*()[]\\|;'\"_<>?`~", "okeey")
        ]

        for i, o in i_o:
            self.assertEqual(Utils.remove_symbols(i), o)
    
    def test__get_random_string__verify_return_length_and_is_alpha_numeric(self):
        """ Verify '_get_random_string'
        """

        valid_chars = set(string.ascii_letters + string.digits)
        for v in [3, 7, 11]:
            text = Utils.get_random_string(string_length=v)
            self.assertEqual(len(text), v)
            self.assertTrue(set(text).issubset(valid_chars))


if __name__ == "__main__":
    unittest.main()
