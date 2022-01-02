import random
import itertools
import time


class Player:
    list_cells = dict.fromkeys(itertools.product(range(3), range(3)), ' ')

    def __init__(self, user, team):
        self.team = team
        self.user = user
        self.rival = "XO".strip(team)

    def play_user(self):
        if self.user == "easy":
            x, y = random.choice(list(dict(filter(lambda i: i[1] == ' ', self.list_cells.items()))))
            print('Making move level "easy"')
        elif self.user == "medium":
            x, y = self.search_cell()
            print('Making move level "medium"')
        elif self.user == "hard":
            start = time.process_time()
            x, y = tuple(self.minimax(self.team))[0]
            end = time.process_time()
            print('Making move level "hard"')
            print(end - start)
        else:
            while True:
                try:
                    x, y = map(int, input("Enter the coordinates: ").split())
                    value = self.list_cells[(x - 1, y - 1)]
                except ValueError:
                    print("You should enter numbers!")
                except IndexError:
                    print("Coordinates should be from 1 to 3!")
                else:
                    if value != ' ':
                        print("This cell is occupied! Choose another one!")
                    else:
                        x -= 1
                        y -= 1
                        break
        self.list_cells[(x, y)] = self.team
        list_check = self.generate()
        return self.check(self.team, list_check)

    def cell_empty(self):
        return list(dict(filter(lambda x: x[1] == ' ', self.list_cells.items())))

    def search_cell(self):
        aux = self.level_medium(self.team)
        if aux:
            return aux
        else:
            aux = self.level_medium(self.rival)
            if aux:
                return aux
            else:
                return random.choice(list(dict(filter(lambda i: i[1] == ' ', self.list_cells.items()))))

    def level_medium(self, word):
        list_check = self.generate()
        for i in list_check:
            w = ''.join(i.values())
            if w.count(word) == 2 and ' ' in w:
                return tuple(dict(filter(lambda x: x[1] == ' ', i.items())))[0]
        return False

    def check(self, player, list_check):
        for i in list_check:
            if all(map(lambda x: x == player, i.values())):
                return f"{self.team} wins"
        return False

    def generate(self):
        list_check = []
        for i in range(3):
            list_check.append(dict(filter(lambda x: x[0][0] == i, self.list_cells.items())))
            list_check.append(dict(filter(lambda x: x[0][1] == i, self.list_cells.items())))
        list_check.append(dict(filter(lambda x: x[0][0] == x[0][1], self.list_cells.items())))
        list_check.append({key: self.list_cells[key] for key in [(2, 0), (1, 1), (0, 2)]})
        return list_check

    def minimax(self, player):
        avail_spots = self.cell_empty()
        list_check = self.generate()
        if self.check(self.team, list_check):
            return {' ': 10}
        elif self.check(self.rival, list_check):
            return {' ': -10}
        elif len(avail_spots) == 0:
            return {' ': 0}

        moves = {}
        for i in avail_spots:
            self.list_cells[i] = player
            if player == self.team:
                y = list(self.minimax(self.rival).values())[0]
            else:
                y = list(self.minimax(self.team).values())[0]
            self.list_cells[i] = ' '
            moves.update({i: y})

        if player == self.team:
            k = max(moves, key=moves.get)
            return {k: moves[k]}
        else:
            k = min(moves, key=moves.get)
            return {k: moves[k]}


def draw(list_tic):
    print("---------")
    for v, i in list_tic.items():
        if v[1] == 0:
            print('|', i, end=' ')
        elif v[1] == 2:
            print(i, '|')
        else:
            print(i, end=' ')
    print("---------")


def main():
    parameters = ["easy", "user", "medium", "hard"]
    while True:
        command = input("Input command: ")
        if command == "exit":
            break
        else:
            try:
                command, user1, user2 = command.split()
                if command != "start" or user1 not in parameters or user2 not in parameters:
                    raise ValueError
            except ValueError:
                print("Bad parameters!")
            else:
                Player.list_cells = dict.fromkeys(itertools.product(range(3), range(3)), ' ')
                play1 = Player(user1, 'X')
                play2 = Player(user2, 'O')
                draw(Player.list_cells)
                for i in range(9):
                    if not i % 2:
                        value = play1.play_user()
                    else:
                        value = play2.play_user()
                    draw(Player.list_cells)
                    if value:
                        print(value)
                        break
                else:
                    print("Draw")


if __name__ == '__main__':
    main()
