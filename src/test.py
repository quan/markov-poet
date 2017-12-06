import unittest

from Markov import Markov, UntrainedModelError


class TestMarkov(unittest.TestCase):

    def setUp(self):
        self.markov = Markov()

    def test_untrained_model(self):
        exception_thrown = False

        try:
            self.markov.generate()
        except UntrainedModelError:
            exception_thrown = True

        self.assertTrue(exception_thrown)


if __name__ == '__main__':
    unittest.main()
