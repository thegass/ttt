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
            'X' : 0b000000000,
            'O' : 0b000000000
        }
        self.starter = self.getStarter()
        self.winner = False
        self.player = self.starter

    def getStarter(self):
        return ('X', 'O')[random.randint(0, 1)]

    def switchPlayer(self):
        self.player=('X','O')[self.player=='X']

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

    

    def transformCoordinates(self, move):
        """transform x,y to binary"""
        return self.moves[move]


if __name__ == '__main__':
    game = Board()
    while game.winner==False:
        move= input('Move for '+game.player+': ')
        game.state[game.player] |= game.transformCoordinates(move)
        game.print()
        game.switchPlayer()


    # print(bin(game.getEmptyCells())[1])
