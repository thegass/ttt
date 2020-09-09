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

    moves = {
        '1,1': 0b100000000,
        '1,2': 0b010000000,
        '1,3': 0b001000000,
        '2,1': 0b000100000,
        '2,2': 0b000010000,
        '2,3': 0b000001000,
        '3,1': 0b000000100,
        '3,2': 0b000000010,
        '3,3': 0b000000001
    }

    possible_moves = {}

    depth = 0

    winners = {
        0b111000000, 0b000111000, 0b000000111,
        0b100100100, 0b010010010, 0b001001001,
        0b100010001, 0b001010100
    }

    state = {}
    rounds = {}
    winner = False
    draw = False
    starter = ''
    player = ''

    def __init__(self):
        self.reset_game()

    def reset_game(self):
        """

        """
        self.state = {
            'X': 0b000000000,
            'O': 0b000000000
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
        self.get_player_names()
        self.play_game()

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
        return ~(self.state['X'] | self.state['O']) & ((1 << 9) - 1)

    def print_board(self):
        """

        """
        # display board
        print()
        divider = '+---+---+---+'
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
            if count == 3:
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

    moveValues = {
        '1,1': -100,
        '1,2': -100,
        '1,3': -100,
        '2,1': -100,
        '2,2': -100,
        '2,3': -100,
        '3,1': -100,
        '3,2': -100,
        '3,3': -100
    }

    def eval_ai_move(self, move, pre_value):
        """

        :param move:
        :param pre_value:
        :return:
        """
        eval_board = TicTacToe()
        eval_board.depth = self.depth + 1
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
            factor=1000
        else:
            factor=1000 - self.depth
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
            for move_id, move in self.possible_moves.items():
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
