
import pandas as pd
import random as r

from data.dictionary import get_words


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class Wordle:
    @classmethod
    def get_proposal(cls, green: dict[int, str], yellow: dict[int, list[str]], gray: list[str]) -> str:
        _, proposals = cls.get_wordle(green, yellow, gray)
        return str(r.choice(list(proposals["word"])))

    @classmethod
    def get_solution(cls, green: dict[int, str], yellow: dict[int, list[str]], gray: list[str], count: int = None) -> str:
        words, proposals = cls.get_wordle(green, yellow, gray, count)
        answer = ''
        if len(proposals["word"]) != 0:
            answer += f'Try to input:\n{" or ".join(proposals["word"])}\n'
        answer += f'Most probable words by ascending:\n{" or ".join(words["word"])}'
        return answer

    @classmethod
    def get_wordle(cls, green: dict[int, str], yellow: dict[int, list[str]], gray: list[str], count: int = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        positions = cls.__get_positions(green, yellow, gray)
        words = cls.__words_chances(positions, count)
        proposals = cls.__propose(words.iloc[0]["word"], green, yellow, gray, count)
        return words, proposals

    @staticmethod
    def __get_positions(green: dict[int, str], yellow: dict[int, list[str]], gray: list[str]) -> list[dict[str, int]]:
        positions: list[dict[str, int]] = []
        for i in range(5):
            position = dict()
            if i in green.keys():
                green_letter = green[i]
                for letter in ALPHABET:
                    if letter == green_letter:
                        position[letter] = 1
                    else:
                        position[letter] = 0
            else:
                for letter in ALPHABET:
                    count = 0
                    if not letter in gray and not letter in yellow[i]:
                        for word in get_words():
                            if word[i] == letter:
                                count += 1
                    position[letter] = count
            positions.append(position)
        return positions

    @classmethod
    def __words_chances(cls, positions: list[dict[str, int]], count: int) -> pd.DataFrame:
        words = pd.DataFrame(columns=["word", "chance"])
        words["word"] = get_words()
        for i, word in enumerate(get_words()):
            chance = 1
            for i1, letter in enumerate(word):
                chance *= cls.__letter_chance(positions, i1, letter)
            words.loc[i, "chance"] = chance

        try:
            return words.sort_values(by="chance", ascending=False).loc[words["chance"] > 0].iloc[range(0, count)]
        except (IndexError, TypeError):
            return words.sort_values(by="chance", ascending=False).loc[words["chance"] > 0]

    @staticmethod
    def __letter_chance(positions: list[dict[str, int]], position: int, letter: str) -> float:
        return positions[position][letter] / sum(positions[position].values())

    @classmethod
    def __propose(cls, relative_word, green: dict[int, str], yellow: dict[int, list[str]], gray: list[str], count: int) -> list[str]:
        relative_letters: list[str] = []
        for i, relative_letter in enumerate(relative_word):
            if i in green:
                gray.append(relative_letter)
                yellow[i] += [letter for el in yellow.values() for letter in el]
            else:
                relative_letters.append(relative_letter)

        realised_positions = cls.__get_positions(dict(), yellow, gray)

        proposals = pd.DataFrame(columns=["word", "chance"])
        proposals["word"] = get_words()
        for i, word in enumerate(get_words()):
            chance = 1
            for relative_letter in relative_letters:
                if not relative_letter in word:
                    chance -= 1/len(relative_letters)
            for i1, letter in enumerate(word):
                chance *= cls.__letter_chance(realised_positions, i1, letter)
            proposals.loc[i, "chance"] = chance
        try:
            return proposals.sort_values(by="chance", ascending=False).loc[proposals["chance"] > 0].iloc[range(0, count)]
        except (IndexError, TypeError):
            return proposals.sort_values(by="chance", ascending=False).loc[proposals["chance"] > 0]
