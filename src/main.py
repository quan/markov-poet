from Markov import Markov


def main():
    markov = Markov()
    markov.train()
    # print(markov.debug_graph_string())
    print(markov.generate())
    # print(markov.debug_language_string())

if __name__ == '__main__':
    main()
