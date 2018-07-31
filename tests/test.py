"""Unit tests for the Markov model."""
import unittest

from markov import Markov, UntrainedModelError


class TestMarkov(unittest.TestCase):

    def setUp(self):
        self.markov = Markov()

    def test_invalid_randomness(self):
        """Test that generator creation fails with invalid randomness values."""
        with self.assertRaises(ValueError):
            self.markov.make_generator(-200)
        with self.assertRaises(ValueError):
            self.markov.make_generator(-0.1)
        with self.assertRaises(ValueError):
            self.markov.make_generator(40)
        with self.assertRaises(ValueError):
            self.markov.make_generator(1.1)

    def test_untrained_model(self):
        """Test that generating with an untrained model raises an exception."""
        with self.assertRaises(UntrainedModelError):
            self.markov.make_generator()

# class TestGeneration(unittest.TestCase):
    

if __name__ == '__main__':
    unittest.main()
