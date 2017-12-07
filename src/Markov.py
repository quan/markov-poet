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

from functools import reduce
from enum import Enum
import random

from haiku_loader import HaikuLoader

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
    START = '*'
    END = '\n'


class Markov:
    """
    Models a Markov chain for poems representings words as states with emphasis
    on line breaks.
    """
    def __init__(self, order=1):
        # The number of previous states the Markov Chain will consider.
        # Values above 2 are not recommended.
        self.order = order
        # A set of all of the words in the language.
        self.language = set()
        # A mapping of words to a list of words that follow.
        self.graph = {}

    def train(self, filename):
        """
        Train the model with a set of data read from a file.
        """
        raise NotImplementedError

    def add_line(self, line):
        """
        Add the words of a line to the chain.
        """
        words = [Token.START] + line.split() + [Token.END]

        # Define each word in the language and save word pairings in the graph.
        # Don't iterate over the closing new line token.
        for i in range(len(words) - 1):
            word = words[i]
            next_word = words[i + 1]

            if word not in self.language:
                self.language.add(word)
                self.graph[word] = []

            self.graph[word].append(next_word)

    def add_poem_as_list(self, poem):
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
        self.add_poem_as_list(poem_lines)

    def generate(self, lines=3, randomness=0):
        """
        Generate a poem from the training data with the given number of lines.
        Return the poem as a list of lines.
        """
        if randomness < -EPSILON or randomness - 1.0 > EPSILON:
            raise ValueError("Randomness should be a value between 0.0 and 1.0, inclusive")

        if len(self.graph.keys()) == 0:
            raise UntrainedModelError

        poem = []

        for _ in range(lines):
            poem.append(self.generate_line())

        return poem

    def generate_formatted(self, lines=3, randomness=0):
        """
        Generate a poem based on the training data with the given number of lines.
        Return the poem as a string.
        """
        generated_lines = self.generate(lines, randomness)
        formatted_poem = '\n'.join(generated_lines)

        return formatted_poem

    def generate_line(self, randomness=0):
        """Generate a single line in a poem."""
        words = []

        # Select the first word by beginning with the start token.
        state = Token.START
        next_state = self._next_state(state)

        # Follow the chain until a newline is reached.
        while next_state is not Token.END:
            state = next_state
            words.append(state)
            next_state = self._next_state(state)

        line = ' '.join(words)

        return line

    def _next_state(self, state):
        """Randomly select the next state for a given state."""
        possible_states = tuple(self.graph[state])
        next_state = random.choice(possible_states)

        return next_state

    def debug_language_string(self):
        """Create and return a string containing the language data."""
        return sorted(list(self.language))

    def debug_graph_string(self):
        """Create and return a string containing the graph data."""
        debug_string = ''

        for word, next_words in self.graph.items():
            debug_string += '{}: {}\n'.format(word, next_words)

        debug_string += 'order of {}'.format(self.order)

        return debug_string
