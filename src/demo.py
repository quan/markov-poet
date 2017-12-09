from Markov import Markov
from haiku_loader import HaikuLoader

import random
import argparse


def main(args):
    markov = Markov(args.order)

    if args.filename is None:
        print('No filename provided')
        return
    else:
        markov.add_file(args.filename)

    # Create a generator from the model with the given randomness.
    generator = markov.generator(args.randomness)

    for _ in range(args.number):
        print(generator.generate_formatted())
        print()


def create_parser():
    parser = argparse.ArgumentParser(description='Poem generator command line tools.')

    # Not yet implemented.
    #
    # parser.add_argument('-v', '--verbose',
    #                     action='store_const',
    #                     const=True, default=False,
    #                     help='keep you updated as stuff happens')
    parser.add_argument('-f', type=str,
                        dest='filename',
                        help='specify a file to read from')
    parser.add_argument('-o', type=int,
                        dest='order', default=1,
                        help='specify the order of the Markov chain')
    parser.add_argument('-r', type=float,
                        dest='randomness', default=0.0,
                        help='introduce some randomness (between 0.0 and 1.0)')
    parser.add_argument('-n', type=int,
                        dest='number', default=1,
                        help='Print more than one haiku')

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)
