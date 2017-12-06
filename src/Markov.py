# from functools import reduce
import functools
from enum import Enum

from haiku_loader import HaikuLoader


class Token(Enum):
    NEWLINE = '\n'
    END = '\n\n'


class Markov:
    '''
    Models a Markov chain.
    '''

    def __init__(self, order=1):
        # The number of previous states the Markov Chain will consider.
        # Values above 2 are not recommended.
        self.order = order
        # A mapping of states to a list of possible following states.
        self.graph = {}
        print("initialized")

    def train(self, filename=None):
        '''
        '''
        if filename is None:
            self._train_default()

        return

    def _train_default(self):
        '''
        Trains the model using the default example data set.
        '''
        data = []

        loader = HaikuLoader()
        lines = loader.get_all_lines()

        # Merge all of the lines, adding a new line token after each line to
        # teach the model some notion of line endings.
        for line in lines:
            list_of_words = line.split()
            data.extend(list_of_words)
            # data.append(Token.NEWLINE)
            data.append('\n')

        # Duplicate the beginning of the data and add it to the end to prevent early end of data.
        count = len(data)
        data_iter = iter(data)
        for i in range(self.order):
            data.extend(next(data_iter))

        for i in range(count):
            word = data[i]
            next_word = data[i + 1]

            if word not in self.graph:
                self.graph[word] = []

            self.graph[word].append(next_word)

    def debug_string(self):
        '''
        Create and return a debug string containing the graph data.
        '''
        debug_string = ''

        for word, next_words in self.graph.items():
            debug_string += '{}: {}\n'.format(word, next_words)

        debug_string += 'order of {}'.format(self.order)

        return debug_string
