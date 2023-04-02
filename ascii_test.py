import unittest
from ascii import AsciiScreen


class AsciiScreenTest(unittest.TestCase):
    def test_write_to_screen_with_illegal_coordinates(self):
        s = AsciiScreen(width=2, height=2)
        s.write_to_screen("t", 0, 0)
        s.write_to_screen("t", 1, 1)
        self.assertRaises(ValueError, lambda: s.write_to_screen("t", -1, 0))
        self.assertRaises(ValueError, lambda: s.write_to_screen("t", 0, -1))
        self.assertRaises(ValueError, lambda: s.write_to_screen("t", 2, 0))
        self.assertRaises(ValueError, lambda: s.write_to_screen("t", 0, 2))


if __name__ == "__main__":
    unittest.main()
