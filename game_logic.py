class GameLogic:
    def __init__(self, word : str):
        self.answer = ""
        self.word = word.lower()
        self.guesses = set()
        self.attemps = 6
        self.used_letters = set()


    def guess_letter(self, letter) -> int:

        if letter in self.used_letters:
            self.attemps -= 1
            return 1 # Было
        self.used_letters.add(letter)
        if letter in self.word:
            self.guesses.add(letter)
            return 2 # верно
        else:
            self.attemps -= 1
            return 3 # неверно


