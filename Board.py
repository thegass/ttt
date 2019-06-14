import random


class Board():
    pieces = {
        'X': ' X ',
        'O': ' O ',
        '.': '   '
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

    winners = {
        0b111000000, 0b000111000, 0b000000111,
        0b100100100, 0b010010010, 0b001001001,
        0b100010001, 0b001010100
    }

    def __init__(self):
        self.state = {
            'X': 0b000000000,
            'O': 0b000000000
        }
        self.rounds = {
            'X': 0,
            'O': 0
        }
        self.starter = self.getStarter()
        self.winner = False
        self.player = self.starter

    def getStarter(self):
        return ('X', 'O')[random.randint(0, 1)]

    def switchPlayer(self):
        self.player = ('X', 'O')[self.player == 'X']

    def getEmptyCells(self):
        return ~(self.state['X'] | self.state['O']) & ((1 << 9)-1)

    def print(self):
        # display board
        divider = '+---+---+---+'
        print(divider)
        count = 0
        line = ''
        for value in self.moves.values():
            line += '|'
            if (value & self.state['O']):
                line += self.pieces['O']
            if (value & self.state['X']):
                line += self.pieces['X']
            if (value & self.getEmptyCells()):
                line += self.pieces['.']
            count += 1
            if (count == 3):
                line += '|'
                print(line)
                count = 0
                print(divider)
                line = ''

    def move(self):
        move = input('Move for '+game.player+': ')
        moveMask = self.transformCoordinates(move)
        if (moveMask == False):
            self.move()
        else:
            if (self.isMovePossible(moveMask)):
                self.state[self.player] |= moveMask
            else:
                print('move not possible')
                self.move()

    def isMovePossible(self, moveMask):
        empty = self.getEmptyCells()
        return moveMask & empty

    def playGame(self):
        self.print()
        while self.winner == False:
            self.rounds[self.player] += 1
            self.move()
            self.print()
            self.checkForWinner()
            self.switchPlayer()

    def checkForWinner(self):
        print('check for win')
        for possibleWin in self.winners:
            if ((possibleWin & self.state[self.player]) == possibleWin):
                print("Winner is player "+self.player+", needed " +
                      str(self.rounds[self.player])+" rounds to win")
                self.winner = self.player

    def transformCoordinates(self, move):
        """transform x,y to binary"""
        if move in self.moves.keys():
            return self.moves[move]
        else:
            print('move out of range')
            return False


if __name__ == '__main__':
    game = Board()
    game.playGame()

    # print(bin(game.getEmptyCells())[1])
