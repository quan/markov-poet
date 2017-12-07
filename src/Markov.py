# MIT License

# Copyright (c) 2017 Quan Tran

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from enum import Enum
from functools import reduce
import random

EPSILON = 0.000001


class UntrainedModelError(Exception):
    """
    An exception raised when the model's generate method is called with
    insufficient training data.
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = "Insufficient data was provided to the Markov model"

        super(UntrainedModelError, self).__init__(msg)


class Token(Enum):
    """
    Used to model special tokens in text: the start of a line and a newline.
    """
    START = '*'
    NEWLINE = '\n'


class Markov:
    """
    Models a Markov chain for poems representings words as states with emphasis
    on line breaks.
    """
    def __init__(self, order=1):
        # The number of previous states the Markov Chain will consider.
        # Values above 2 are not recommended.
        self.order = order
        
        # A mapping of words to a list of words that follow.
        self.graph = {}

    def add_file(self, filename):
        """
        Train the model with a corpus read from a file.
        """
        with open(filename, 'r') as file:
            text = file.read()
            self.add_poem(text)

    def add_line(self, line):
        """
        Add the words of a line to the chain.
        """
        words_in_line = list(map(lambda x: x.lower(), line.split()))
        tokens = [Token.START] + words_in_line + [Token.NEWLINE]

        # Save word pairings in the graph to build the chain.
        # Stop before the closing new line token to prevent IndexOutOfBounds.
        for i in range(len(tokens) - 1):
            word = tokens[i]
            next_word = tokens[i + 1]

            # Add each word to the language.
            if word not in self.graph:
                self.graph[word] = []

            # Prevent empty lines from being added to the graph.
            if word is not Token.START or next_word is not Token.NEWLINE:
                self.graph[word].append(next_word)

    def add_lines(self, poem):
        """
        Add the words in a poem to this Markov model's data.
        Expects a list of strings, where each string is a line in a poem.
        """
        for line in poem:
            self.add_line(line)

    def add_poem(self, poem):
        """
        Add the words in a poem to this Markov model's data.
        Expects a poem as a multi-line string.
        """
        poem_lines = poem.split('\n')
        self.add_lines(poem_lines)

    def generator(self, randomness=0.0):
        """Return a poem generator for the Markov model with some randomness."""
        return self.Generator(self.graph, randomness)

    class Generator:
        """
        A class that generates poems based on a given chain.
        """
        def __init__(self, graph, randomness):
            if not -EPSILON < randomness < 1.0 + EPSILON:
                raise ValueError("Randomness should be a value between 0.0 and 1.0, inclusive")

            self.graph = graph

            # The amount of randomness introduced into word generation.
            self.randomness = randomness

            # A representative sample of all of the possible states in the chain.
            # self.random_sample = reduce(lambda x, y: x + y, graph.values())
            self.random_sample = []
            for values in graph.values():
                self.random_sample.extend(values)

        def generate(self, lines=3):
            """
            Generate a poem from the training data with the given number of lines.
            Return the poem as a list of lines.
            """
            if len(self.graph.keys()) == 0:
                raise UntrainedModelError

            poem = []

            for _ in range(lines):
                line = self.generate_line()
                poem.append(line)

            return poem

        def generate_formatted(self, lines=3):
            """
            Generate a poem based on the training data with the given number of lines.
            Return the poem as a string.
            """
            generated_lines = self.generate(lines)
            formatted_poem = '\n'.join(generated_lines)

            return formatted_poem

        def generate_line(self):
            """Generate a single line in a poem."""
            words = []

            # Select the first word by beginning with the start token.
            state = self._next_word(Token.START)

            # The nested outer loop and state reset if the words list is empty
            # after the inner loop ensures that at least one word is generated.
            while not words:
                while state is not Token.NEWLINE:
                    words.append(state)
                    state = self._next_word(state)

                if not words:
                    state = self._next_word(Token.START)

            line = ' '.join(words)

            return line

        def _next_word(self, state):
            """Randomly select the next word for a given state or simply a random word."""
            if random.random() < self.randomness:
                possibilities = tuple(self.random_sample)
            else:
                possibilities = tuple(self.graph[state])

            next_word = random.choice(possibilities)

            return self._next_word(state) if next_word is Token.START else next_word

        def test_next_word(self):
            """
            Tests the asymptotic probabability of randomly selecting a new line.
            """
            sample_size = 10000
            number_of_newlines = 0
            state = Token.START

            for i in range(sample_size):
                state = self._next_word(state)
                if state is Token.NEWLINE:
                    number_of_newlines = number_of_newlines + 1
                    i = i + 1
                    state = Token.START
                    continue

            print("out of {} samples, {} were of newlines".format(sample_size, number_of_newlines))

    def debug_string(self):
        """Create and return a string containing the graph data."""
        debug_string = ''

        for word, next_words in self.graph.items():
            debug_string += '{}: {}\n'.format(word, next_words)

        debug_string += 'order of {}'.format(self.order)

        return debug_string
