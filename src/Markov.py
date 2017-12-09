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
        # The number of words the chain will consider for its current state.
        # Values above 2 are not recommended.
        self.order = order
        # A mapping of states to a list of words that follow.
        self.graph = {}
        self.graph[Token.START] = []
        # A collection of all of the encountered states.
        # self.states = []

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

        TODO: strip punctuation from words/states. Maybe.
        """
        words_in_line = list(map(lambda x: x.lower(), line.split()))
        tokens = words_in_line + [Token.NEWLINE]

        # Don't process the line if the line is too short.
        if len(tokens) <= self.order:
            return
        # Add the starting state to the graph.
        else:
            starting_state = tuple(tokens[0:self.order])
            self.graph[Token.START].append(starting_state)

        # Set keys to be states (tuples) of size equal to the order.
        # For each state, save the next word.
        for i in range(len(tokens) - self.order):
            state = tuple(tokens[i:i + self.order])
            next_word = tokens[i + self.order]

            # Add each state to the language.
            if state not in self.graph:
                self.graph[state] = []

            # Add the state to the aggregate population for random sampling.
            # self.states.append(state)
            # Add the next word to the state's list of next states.
            self.graph[state].append(next_word)

    def add_lines(self, poem):
        """
        Add the words in a poem to the chain's data.
        Expects a poem as a list of lines.

        e.g. ['old pond', 'frog leaping', 'splash']
        """
        for line in poem:
            self.add_line(line)

    def add_poem(self, poem):
        """
        Add the words in a poem to the chain's data.
        Expects a poem as a multi-line string.

        e.g. '''the piano room
        pure ivory keys
        under a layer of dust'''
        """
        poem_lines = poem.split('\n')
        self.add_lines(poem_lines)

    def generator(self, randomness=0.0):
        """
        Create a poem generator for the Markov model with some randomness.
        """
        # Randomness is not supported for chains of order greater than 1
        # because I haven't decided how to implement it yet.
        if self.order > 1:
            randomness = 0.0

        return self.Generator(self.graph, randomness)

    class Generator:
        """
        A class that generates poems based on a given chain.

        graph: the data for the chain
        randomness: the amount of randomness to introduce into state selection
        """
        def __init__(self, graph, randomness):
            if not -EPSILON < randomness < 1.0 + EPSILON:
                raise ValueError("Randomness should be a value between 0.0 and 1.0, inclusive")

            self.randomness = randomness

            if not graph.keys():
                raise UntrainedModelError

            self.graph = graph

        def generate(self, lines=3):
            """
            Generate a poem from the training data with the given number of lines.
            Return the poem as a list of lines.
            """
            poem = []

            for i in range(lines):
                blank = True if 0 < i < lines - 1 else False
                line = self.generate_line(blank)
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

        def generate_line(self, blank=True):
            """
            Generate a single line in a poem.
            """
            words = []

            # Select the first state by beginning with the start token.
            starting_states = tuple(self.graph[Token.START])
            state = random.choice(starting_states)
            words.extend(list(state))
            next_word = self._next_word(state)

            # This loop builds the words list until a newline is encountered.
            while next_word is not Token.NEWLINE:
                words.append(next_word)
                state = state[1:] + (next_word,)
                next_word = self._next_word(state)

            # This loop ensures that at least one word is selected if the line
            # should not be blank.
            # The probability of initially selecting a newline is directly
            # proportional to increased generator randomness.
            # if not blank:
            #     while state is Token.NEWLINE:
            #         state = self._next_word(state)

            line = ' '.join(words)

            return line

        def _next_word(self, state):
            """
            Randomly select the next word for a given state or -- based on the
            randomness factor -- simply a random word.
            """
            if random.random() < self.randomness:
                possibilities = tuple(self.random_sample)
            else:
                possibilities = tuple(self.graph[state])

            next_word = random.choice(possibilities)

            return next_word

    def debug_string(self):
        """Create and return a string containing the graph data."""
        debug_string = ''

        for word, next_words in self.graph.items():
            debug_string += '{}: {}\n'.format(word, next_words)

        debug_string += 'order of {}'.format(self.order)

        return debug_string
