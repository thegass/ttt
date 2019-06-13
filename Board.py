class Board():
    def __init__(self):
        self.stateX = 0b000000000
        self.stateO = 0b000000000

    def setPiece(self, player, position):
        """update state"""

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

    def transformCoordinates(self, move):
        """transform x,y to binary"""
        return self.moves[move]
