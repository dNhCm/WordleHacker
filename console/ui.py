from copy import deepcopy

from pyfiglet import print_figlet

from wordle.wordle import Wordle


class UI:
    def __init__(self):
        self.green: dict[int, str] = dict()
        self.yellow: dict[int, list[str]] = {0: [], 1: [], 2: [], 3: [], 4: []}
        self.gray: list[str] = []
        self.main()

    def command_handler(self, command: str):
        command = command.lower()
        if "update" in command:
            args = command.split(' ')[1:]

            for i, arg in enumerate(args):
                letter = arg[0]
                color = arg[1:]
                if color == "gn":
                    self.green[i] = letter
                elif color == "y":
                    self.yellow[i].append(letter)
                elif color == "gy":
                    self.gray.append(letter)
                else:
                    print(f"{color} is undefined color!")
            print(Wordle.get_solution(deepcopy(self.green), deepcopy(self.yellow), deepcopy(self.gray), 10))
        elif "new game" in command:
            self.green = dict()
            self.yellow = {0: [], 1: [], 2: [], 3: [], 4: []}
            self.gray = []
        elif "help" in command:
            print("update - command to update green, yellow gray letters\n"
                  "Form: update [word][gn (green), y (yellow), or gy (gray)]\n"
                  "Usage: (saint) > update sgy agn iy ngy tgy\n")
            print("new game - reset states of letters\n"
                  "Form: new game\n"
                  "Usage: new game")
        else:
            print(f"{command} is undefined command!\nTry to text help")
        print('\n')

    def main(self):
        print_figlet("Wordle Hacker", font="cricket", colors="magenta")
        print('\n Input help to know commands; Input update to update')
        while True:
            self.command_handler(input('> '))


def console_main():
    UI()
