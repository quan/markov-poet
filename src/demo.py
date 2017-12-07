from Markov import Markov
from haiku_loader import HaikuLoader


def main():
    poemarkov = Markov()

    loader = HaikuLoader()
    haiku_list = loader.get_all()

    for haiku in haiku_list:
        poemarkov.add_poem_as_list(haiku)

    for _ in range(5):
        print(poemarkov.generate_formatted())
        print()


if __name__ == '__main__':
    main()
