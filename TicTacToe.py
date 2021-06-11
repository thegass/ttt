#!/usr/bin/env python3

import random


class TicTacToe:
    pieces = {
        'X': ' X ',
        'O': ' O ',
        '.': '   '
    }

    ai_players = {
        'X': False,
        'O': False
    }

    playerNames = {
        'X': '',
        'O': ''
    }

    size = 3

    moves = {}

    moveValues = {
    }

    possible_moves = {}

    depth = 0

    winners = []

    state = {}
    rounds = {}
    winner = False
    draw = False
    starter = ''
    player = ''

    def init_moves(self):
        self.generate_moves()
        self.generate_winners()
        self.reset_game()

    def generate_moves(self):
        if (len(self.moves) == 0):
            index = self.size**2
            for x_index in range(1, self.size + 1):
                for y_index in range(1, self.size + 1):
                    index -= 1
                    self.moves[str(x_index)+','+str(y_index)] = 2**index
                    self.moveValues[str(x_index)+','+str(y_index)] = -100

    def generate_winners(self):
        diagonal_winner1 = 0
        diagonal_winner2 = 0
        index = 0
        if (len(self.winners) == 0):
            y_winners = dict()
            for x_index in range(1, self.size + 1):
                x_winner = 0
                for y_index in range(1, self.size + 1):
                    index += 1
                    value = self.moves[str(x_index)+','+str(y_index)]
                    x_winner += value
                    if y_index in y_winners:
                        y_winners[y_index] += value
                    else:
                        y_winners[y_index] = value
                    if (x_index == y_index):
                        diagonal_winner1 += self.moves[str(
                            x_index)+','+str(y_index)]
                    if (x_index+y_index == (self.size+1)):
                        diagonal_winner2 += self.moves[str(
                            x_index)+','+str(y_index)]

                self.winners.append(x_winner)
            for y_winner in y_winners.values():
                self.winners.append(y_winner)
            self.winners.append(diagonal_winner1)
            self.winners.append(diagonal_winner2)
            print(repr(self.winners))

    def reset_game(self):
        """

        """
        self.state = {
            'X': 0,
            'O': 0
        }
        self.rounds = {
            'X': 0,
            'O': 0
        }
        self.winner = False
        self.draw = False
        self.get_starter()

    def main_loop(self):
        """

        """
        print('T-T-T')
        self.get_board_size()
        self.init_moves()
        self.get_player_names()
        self.play_game()

    def get_board_size(self):
        """

        """
        size = input('board size?')
        if size.isdigit():
            self.size = int(size)
        else:
            self.get_board_size()

    def get_player_names(self):
        """

        """
        for player in ['X', 'O']:
            player_name = input('name for player ' + player +
                                '(press enter f. AI)?')
            if player_name == '':
                self.ai_players[player] = True
                self.playerNames[player] = 'AI_' + player
            else:
                self.playerNames[player] = player_name

    def play_game(self):
        """

        """
        self.reset_game()
        while (self.winner is False) and (self.draw is False):
            self.rounds[self.player] += 1
            self.move()
            self.print_board()
            self.check_for_winner()
            self.switch_player()
        if self.draw:
            print("Draw")
        if self.winner:
            print("Winner is player " +
                  self.playerNames[self.winner] +
                  ", needed " +
                  str(self.rounds[self.winner]) +
                  " rounds to win")

    def get_starter(self):
        """

        """
        self.starter = ('X', 'O')[random.randint(0, 1)]
        self.player = self.starter

    def switch_player(self):
        """

        """
        self.player = ('X', 'O')[self.player == 'X']

    def get_empty_cells(self):
        """

        :return:
        """
        return ~(self.state['X'] | self.state['O']) & ((1 << (self.size**2)) - 1)

    def print_board(self):
        """

        """
        # display board
        print()
        divider = '+'
        for col in range(0, self.size):
            divider += '---+'
        print(divider)
        count = 0
        line = ''
        for value in self.moves.values():
            line += '|'
            if value & self.state['O']:
                line += self.pieces['O']
            if value & self.state['X']:
                line += self.pieces['X']
            if value & self.get_empty_cells():
                line += self.pieces['.']
            count += 1
            if count == self.size:
                line += '|'
                print(line)
                count = 0
                print(divider)
                line = ''

    def move(self):
        """

        :return:
        """
        self.update_possible_moves()
        if not self.possible_moves:
            self.draw = True
            return
        if self.ai_players[self.player] is False:
            move = input('Move for ' + self.playerNames[game.player] + ': ')
            move_mask = self.transform_coordinates(move)
            if not move_mask:
                self.move()
            else:
                if move_mask in self.possible_moves.values():
                    self.state[self.player] |= move_mask
                else:
                    print('move not possible')
                    self.move()
        else:
            move_mask = self.get_ai_move()
            self.state[self.player] |= move_mask

    def check_for_winner(self):
        """

        """
        if not self.draw:
            for possible_win in self.winners:
                if (possible_win & self.state[self.player]) == possible_win:
                    self.winner = self.player

    def eval_ai_move(self, move, pre_value):
        """

        :param move:
        :param pre_value:
        :return:
        """
        eval_board = TicTacToe()
        eval_board.size = self.size
        eval_board.depth = self.depth + 1
        # if (self.depth > self.size*2):
        #    return pre_value
        eval_board.state = self.state.copy()
        eval_board.rounds = self.rounds.copy()
        eval_board.player = self.player
        eval_board.ai_players = {
            'X': True,
            'O': True
        }
        eval_board.state[self.player] |= move
        eval_board.check_for_winner()
        while ((eval_board.winner == False) and (eval_board.draw == False)):
            eval_board.switch_player()
            eval_board.move()
            eval_board.check_for_winner()
        if (self.depth == 0):
            factor = 1+(self.size**2)
        else:
            factor = 1+(self.size**2) - self.depth
        if (eval_board.winner == self.player):
            return pre_value + factor
        else:
            if (eval_board.draw):
                return pre_value + factor/2
            else:
                return pre_value - factor*2

    def reset_move_values(self):
        """

        """
        for key in self.moveValues.keys():
            self.moveValues[key] = -100

    def get_ai_move(self):
        """

        :return:
        """
        move_pool = list(self.possible_moves.values())
        if move_pool:
            if ((self.starter == self.player) and (
                    self.state[self.player] == 0b000000000)):
                return random.choice(move_pool)
            sample_size = self.size*2
            if (sample_size > len(self.possible_moves.items())):
                sample_size = len(self.possible_moves.items())

            random_moves = random.sample(
                tuple(self.possible_moves.items()), sample_size)
            for move_id, move in random_moves:
                self.moveValues[move_id] = self.eval_ai_move(
                    move, self.moveValues[move_id])
            sorted_values = sorted(self.moveValues.items(),
                                   key=lambda x: x[1], reverse=True)
            if self.depth == 0:
                self.reset_move_values()
            for item in sorted_values:
                if item[0] in self.possible_moves.keys():
                    if self.depth == 0:
                        print('AI Move: ' + str(item[0]))
                    return self.possible_moves[item[0]]
            print('no move found')
            return False
        return False

    def is_move_possible(self, move_mask):
        """

        :param move_mask:
        :return:
        """
        empty = self.get_empty_cells()
        return move_mask & empty

    def update_possible_moves(self):
        """

        """
        possible_moves = {}
        for move_id, move in self.moves.items():
            if self.is_move_possible(move):
                possible_moves[move_id] = move
        self.possible_moves = possible_moves

    def get_possible_moves(self):
        """

        :return:
        """
        return self.possible_moves

    def transform_coordinates(self, move):
        """transform x,y to binary"""
        if move in self.moves.keys():
            return self.moves[move]
        print('move out of range')
        return False


if __name__ == '__main__':
    game = TicTacToe()
    game.main_loop()
