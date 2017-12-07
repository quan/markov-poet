from Markov import Markov
from haiku_loader import HaikuLoader

import random


def main():
    markov = Markov()

    # loader = HaikuLoader()
    # haiku_list = loader.get_all()

    filename = "all_haiku_lines.txt"

    # for haiku in haiku_list:
    markov.add_file(filename)
    for i in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        generator = markov.generator(i)
        for _ in range(10):
            print(generator.generate_formatted())
            print()

        print()
        print()
        # generator.test_next_word()
    # for _ in range(10):
    #     number_of_lines = random.randint(2, 4)
    #     print(generator.generate_formatted(number_of_lines))
    #     print()


if __name__ == '__main__':
    main()
