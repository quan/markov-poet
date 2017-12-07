from functools import reduce
from enum import Enum
import random

from haiku_loader import HaikuLoader

EPSILON = 0.000001


class UntrainedModelError(Exception):
    '''
    An exception raised when the model's generate method is called with
    insufficient training data.
    '''

    def __init__(self, msg=None):
        if msg is None:
            msg = "Insufficient data was provided to the Markov model"

        super(UntrainedModelError, self).__init__(msg)


class Token(Enum):
    START = '*'
    NEWLINE = '\n'
    END = '\n\n'


class Markov:
    '''
    Models a Markov chain with words as states.
    '''
    def __init__(self, order=1):
        # The number of previous states the Markov Chain will consider.
        # Values above 2 are not recommended.
        self.order = order
        # A set of all of the words in the language.
        self.language = set()
        # A mapping of words to a list of words that follow.
        self.graph = {}

    def train(self, filename=None):
        '''
        '''
        if filename is None:
            self._train_default()
        else:
            raise NotImplementedError

    def add_to_training_data(self, haiku):
        '''
        Adds the given haiku to this Markov model's data.
        Expects a list of strings, where each string is a line in the haiku.
        '''

        # Create a single list of words with a newline token following each line.
        all_words = reduce(lambda x, y: x + y.split() + [Token.NEWLINE], haiku, [Token.START])

        # Save the word pairings in the graph, skipping newlines.
        for index in range(len(all_words) - 1):
            word = all_words[index]
            next_word = all_words[index + 1]

            if word is Token.NEWLINE:
                continue

            if word not in self.language:
                self.language.add(word)
                self.graph[word] = []

            self.graph[word].append(next_word)

    def generate(self, lines=3, randomness=0):
        '''
        Generates a poem from the training data with the given number of lines.
        Returns the poem as a list of lines.
        '''
        if randomness - 1.0 > EPSILON:
            raise ValueError("Randomness should be a value between 0.0 and 1.0, inclusive")

        if len(self.graph.keys()) == 0:
            raise UntrainedModelError

        poem = []

        for _ in range(lines):
            poem.append(self.generate_line())

        return poem

    def generate_line(self):
        '''
        Generates a single line in a poem.
        '''
        words = []

        # Select the first word by beginning with the start token.
        state = Token.START
        next_state = self._next_state(state)

        # Follow the chain until a newline is reached.
        while next_state is not Token.NEWLINE:
            state = next_state
            words.append(state)
            next_state = self._next_state(state)

        line = ' '.join(words)

        return line

    def _next_state(self, state):
        '''
        Randomly selects the next state for the given state.
        '''
        next_states = tuple(self.graph[state])
        return random.choice(next_states)

    def _train_default(self):
        '''
        Trains the model using the default example data set.
        '''
        loader = HaikuLoader()
        haiku_list = loader.get_all()

        for haiku in haiku_list:
            self.add_to_training_data(haiku)

    def debug_language_string(self):
        '''
        Create and return a string containing the language data.
        '''
        return sorted(list(self.language))

    def debug_graph_string(self):
        '''
        Create and return a string containing the graph data.
        '''
        debug_string = ''

        for word, next_words in self.graph.items():
            debug_string += '{}: {}\n'.format(word, next_words)

        debug_string += 'order of {}'.format(self.order)

        return debug_string

    # def __str__(self):
    #     return self.debug_string()
