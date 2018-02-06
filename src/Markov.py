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
import random

EPSILON = 0.000001


class UntrainedModelError(Exception):
    """
    An exception raised when the model's generate method is called with
    insufficient training data.
    """
    def __init__(self, msg="Insufficient data was provided to the Markov model"):
        super(UntrainedModelError, self).__init__(msg)


class Token(Enum):
    """
    Used to model special tokens in text: the start of a line and a newline.
    """
    START = '*'
    NEWLINE = '\n'


class Markov:
    """
    Models a Markov chain for poems representing states as n-tuples of words.
    Emphasizes line breaks as a sink state in generation.
    """
    def __init__(self, order=1):
        # The number of words the chain will consider for its current state.
        self.order = order
        # A collection of all of the states that may begin a line.
        # Used for selecting a starting point for a chain.
        self.starting_states = []
        # A collection of all of the encountered states used for random sampling.
        self.distribution = []
        # A mapping of each state to a list of words that follow it.
        self.chain = {}

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
        words_in_line = [word.lower() for word in line.split()]
        tokens = words_in_line + [Token.NEWLINE]

        # Only process the line if it is long enough, starting by saving the
        # starting state of the line.
        if len(tokens) > self.order:
            starting_state = tuple(tokens[0:self.order])
            self.starting_states.append(starting_state)
        else:
            return

        # Set keys to be states (tuples) of size equal to the order.
        # For each state, save a list of the words that follow.
        for i in range(len(tokens) - self.order):
            state = tuple(tokens[i:i + self.order])
            next_word = tokens[i + self.order]

            if state not in self.chain:
                self.chain[state] = []

            # Add the state to the aggregate distribution for random sampling.
            self.distribution.append(state)
            # Add the next word to the state's list of next states.
            self.chain[state].append(next_word)

    def add_lines(self, poem):
        """
        Add the words in a poem to the chain's data.
        Expects a poem as a list of lines:

        example = ['old pond', 'frog leaping', 'splash']
        """
        for line in poem:
            self.add_line(line)

    def add_poem(self, poem):
        """
        Add the words in a poem to the chain's data.
        Expects a poem as a multi-line string:

        example = '''the piano room
        pure ivory keys
        under a layer of dust'''
        """
        self.add_lines(poem.split('\n'))

    def generator(self, randomness=0.0):
        """
        Create a poem generator for the chain with some randomness.
        """
        chain = self.chain
        starting_states = self.starting_states
        distribution = self.distribution

        return self.Generator(chain, starting_states, distribution, randomness)

    class Generator:
        """
        A class that generates poems based on a given chain.
        """
        def __init__(self, chain, starting_states, distribution, randomness):
            if not -EPSILON < randomness < 1.0 + EPSILON:
                raise ValueError("Randomness should be a value between 0.0 and 1.0, inclusive")

            if not chain.keys():
                raise UntrainedModelError

            self.randomness = randomness
            # Values from the parent Markov model.
            self.chain = chain
            # Convert to tuples for random selection.
            self.starting_states = tuple(starting_states)
            self.distribution = tuple(distribution)

        def generate(self, start_state=None):
            """
            Return a list of words generated by one walk through the chain.
            """
            # Select a random starting state if one is not provided.
            # This isn't affected by the randomness factor.
            state = start_state or random.choice(self.starting_states)

            # Initialize the returned list of words with the starting state.
            words = list(state)

            next_word, state = self._step(state)
            # Step through the chain, building the list of words in this line
            # until a newline is encountered.
            while next_word is not Token.NEWLINE:
                words.append(next_word)
                next_word, state = self._step(state)

            return words

        def generate_line(self):
            """
            Generate a single line of a poem by walking through the chain.
            """
            return ' '.join(self.generate())

        def generate_lines(self, number_of_lines=3):
            """
            Generate a poem with n lines by walking through the chain n times.
            Return the poem as a list of lines.
            """
            return [self.generate_line() for _ in range(number_of_lines)]

        def generate_formatted(self, number_of_lines=3):
            """
            Generate a poem with n lines by walking through the chain n times.
            Return the poem as a string of n lines.
            """
            return '\n'.join(self.generate_lines(number_of_lines))

        def _step(self, state):
            """
            Given a state, select the next word at random, returning the word
            and constructing the next state.
            """
            # Randomization is achieved by selecting a different state before stepping.
            if random.random() < self.randomness:
                state = random.choice(self.distribution)

            possibilities = tuple(self.chain[state])

            next_word = random.choice(possibilities)
            # Create the next state by adding the next word to the tail of
            # the current state.
            next_state = state[1:] + (next_word,)

            return next_word, next_state

    def debug_string(self):
        """Create and return a string containing the chain data."""
        debug_string = ''

        for word, next_words in self.chain.items():
            debug_string += '{}: {}\n'.format(word, next_words)

        debug_string += 'order of {}'.format(self.order)

        return debug_string
