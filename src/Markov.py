from functools import reduce
from enum import Enum
import random

from haiku_loader import HaikuLoader


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
        # A mapping of words to a list of following words.
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

        # lowercase?

        # Create a single list of words with a newline token following each line.
        all_words = reduce(lambda x, y: x + y.split() + [Token.NEWLINE], haiku, [])

        for index in range(len(all_words) - 1):
            word = all_words[index]
            next_word = all_words[index + 1]

            if word is not Token.NEWLINE:
                self.language.add(word)
                self.graph[word] = []
                self.graph[word].append(next_word)

    def generate(self, lines=3):
        '''
        Generates a poem from the training data with the given number of lines.
        Returns the poem as a list of lines.
        '''
        if len(self.graph.keys()) == 0:
            raise UntrainedModelError

        poem = []

        for _ in range(lines):
            poem.append(self.generate_line())

        return poem

    def generate_line(self):
        '''
        '''
        # Select a random starting word from the language.
        state = random.choice(tuple(self.language))
        print(state)
        next_states = self.graph[state]
        next_state = random.choice(tuple(next_states))
        if next_state is Token.NEWLINE:
            return '1. {}, then newline'.format(state)

        return '1. {}, 2. {}'.format(state, next_state)

    def _train_default(self):
        '''
        Trains the model using the default example data set.
        '''
        loader = HaikuLoader()
        haiku_list = loader.get_all()

        for haiku in haiku_list:
            self.add_to_training_data(haiku)

    def _train_default_backup(self):
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
