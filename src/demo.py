from Markov import Markov
from haiku_loader import HaikuLoader

import random


def main():
    poemarkov = Markov()

    # loader = HaikuLoader()
    # haiku_list = loader.get_all()

    filename = "all_haiku_lines.txt"

    # for haiku in haiku_list:
    poemarkov.add_file(filename)

    for _ in range(10):
        number_of_lines = random.randint(2, 4)
        print(poemarkov.generate_formatted(number_of_lines))
        print()


if __name__ == '__main__':
    main()
