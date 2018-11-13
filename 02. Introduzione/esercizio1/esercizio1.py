import random
import sys
import re

class Esercizio1:

    def __init__(self, argv):
        try:
            self._path = argv[0]
        except:
            self._path = 'words.txt'

    def get_word(self):
        words = open(self._path, 'r').readlines()
        while True:
            word = (random.choice(words)).strip().upper()
            if len(word) > 6:
                break
        return word

    def read_char(self):
        while True:
            char = input(">> ").upper()
            if re.match('[A-Z]$', char, re.IGNORECASE):
                return char
            else:
                print("Error. Write only one letter.")

    def play(self):
        word = self.get_word()
        out = list('_' * len(word))
        num_ok = 0
        lettere_usate = ""
        while num_ok != len(word):
            print(" ".join(out))
            input_char = self.read_char()
            if lettere_usate.find(input_char) == -1:
                lettere_usate += input_char
                pos = [pos for pos, char in enumerate(word) if char == input_char]
                for i in pos:
                    out[i] = input_char
                num_ok += len(pos)
        print("Lettere usate: ", " - ".join(lettere_usate))
        print("La parola è: " + word)


if __name__ == '__main__':
    esercizio = Esercizio1(sys.argv[1:])
    esercizio.play()
