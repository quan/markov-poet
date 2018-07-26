"""Demo driver for the Markov Poet."""
import argparse

from Markov import Markov


def _parse_args():
    parser = argparse.ArgumentParser(description='Poem generator command line tools.')

    # Not yet implemented.
    #
    # parser.add_argument('-v', '--verbose',
    #                     action='store_const',
    #                     const=True, default=False,
    #                     help='keep you updated as stuff happens')
    parser.add_argument('--filename', '-f',
                        help='specify a file to read from',
                        type=str)
    parser.add_argument('--order', '-o',
                        help='specify the order of the Markov chain',
                        type=int, default=1)
    parser.add_argument('--randomness', '-r',
                        help='introduce some randomness (between 0.0 and 1.0)',
                        type=float, default=0.0)
    parser.add_argument('--number', '-n',
                        help='Print more than one haiku',
                        type=int, default=1)
    return parser.parse_args()


def main():
    """Generate a poem."""
    args = _parse_args()
    markov = Markov(args.order)

    if args.filename is None:
        print('No filename provided')
        return

    # Read the file and add its contents to the Markov model.
    markov.add_file(args.filename)

    # Create a generator from the model with the given randomness.
    generator = markov.generator(args.randomness)

    for _ in range(args.number):
        print(generator.generate_formatted())
        print()


if __name__ == '__main__':
    main()
