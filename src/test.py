"""Unit tests for the Markov model."""
import unittest
from Markov import Markov, UntrainedModelError


class TestMarkov(unittest.TestCase):

    def setUp(self):
        self.markov = Markov()

    def test_untrained_model(self):
        """Test that generating with an untrained model raises an exception."""
        with self.assertRaises(UntrainedModelError):
            self.markov.generate()

# class TestGeneration(unittest.TestCase):
    

if __name__ == '__main__':
    unittest.main()
