"""Unit tests for the Markov model."""
import unittest

from markov import Markov, UntrainedModelError


class TestMarkov(unittest.TestCase):

    def setUp(self):
        self.markov = Markov()

    def test_invalid_randomness(self):
        """Test that generator creation fails with invalid randomness values."""
        with self.assertRaises(ValueError):
            self.markov.generator(-200)
        with self.assertRaises(ValueError):
            self.markov.generator(-0.1)
        with self.assertRaises(ValueError):
            self.markov.generator(40)
        with self.assertRaises(ValueError):
            self.markov.generator(1.1)

    def test_untrained_model(self):
        """Test that generating with an untrained model raises an exception."""
        with self.assertRaises(UntrainedModelError):
            self.markov.generator()

# class TestGeneration(unittest.TestCase):
    

if __name__ == '__main__':
    unittest.main()
