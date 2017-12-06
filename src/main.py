from Markov import Markov


def main():
    markov = Markov()
    markov.train()

    print(markov.debug_string())

if __name__ == '__main__':
    main()
