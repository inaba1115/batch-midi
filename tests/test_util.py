import unittest

from batch_midi.util import second2tick


class TestUtil(unittest.TestCase):
    def test_second2tick(self):
        self.assertEqual(second2tick(10.0), 9600)
