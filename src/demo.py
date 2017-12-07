from Markov import Markov
from haiku_loader import HaikuLoader

import random


def main():
    poemarkov = Markov()

    loader = HaikuLoader()
    haiku_list = loader.get_all()

    for haiku in haiku_list:
        poemarkov.add_poem_as_list(haiku)

    for _ in range(10):
        number_of_lines = random.randint(2, 4)
        print(poemarkov.generate_formatted(number_of_lines))
        print()


if __name__ == '__main__':
    main()
