from Markov import Markov


def main():
    markov = Markov()
    markov.train()
    # print(markov.debug_graph_string())
    # print(markov.debug_language_string())
    for _ in range(1000):
        haiku = markov.generate_formatted()
        print(haiku)
        print()

if __name__ == '__main__':
    main()
