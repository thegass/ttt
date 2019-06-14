import random


class TicTacToe():
    pieces = {
        'X': ' X ',
        'O': ' O ',
        '.': '   '
    }

    aiPlayers = {
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

    possibleMoves = {}

    winners = {
        0b111000000, 0b000111000, 0b000000111,
        0b100100100, 0b010010010, 0b001001001,
        0b100010001, 0b001010100
    }

    def __init__(self):
        self.resetGame()

    def resetGame(self):
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
        self.getStarter()

    def mainLoop(self):
        print('T-T-T')
        self.getPlayerNames()
        self.playGame()

    def getPlayerNames(self):
        for player in ['X', 'O']:
            playerName = input('name for player '+player +
                               '(press enter f. AI)?')
            if (playerName == ''):
                self.aiPlayers[player] = True
                self.playerNames[player] = 'AI_'+player
            else:
                self.playerNames[player] = playerName

    def playGame(self):
        self.resetGame()
        self.print()
        while ((self.winner == False) and (self.draw == False)):
            self.rounds[self.player] += 1
            self.move()
            self.print()
            self.checkForWinner()
            self.switchPlayer()

    def getStarter(self):
        self.starter = ('X', 'O')[random.randint(0, 1)]
        self.player = self.starter

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
        self.updatePossibleMoves()
        if not self.possibleMoves:
            self.draw=True
            return
        if (self.aiPlayers[self.player] == False):
            move = input('Move for '+self.playerNames[game.player]+': ')
            moveMask = self.transformCoordinates(move)
            if moveMask == False:
                self.move()
            else:
                if moveMask in self.possibleMoves.values():
                    self.state[self.player] |= moveMask
                else:
                    print('move not possible')
                    self.move()
        else:
            moveMask = self.getAIMove()
            self.state[self.player] |= self.getAIMove()
                

    def isMovePossible(self, moveMask):
        empty = self.getEmptyCells()
        return moveMask & empty

    def checkForWinner(self):
        if self.draw:
            print("Draw after " + str(self.rounds[self.player])+" rounds")
        else:
            for possibleWin in self.winners:
                if ((possibleWin & self.state[self.player]) == possibleWin):
                    print("Winner is player "+self.playerNames[self.player]+", needed " +
                        str(self.rounds[self.player])+" rounds to win")
                    self.winner = self.player

    def getAIMove(self):
        movePool = list(self.possibleMoves.values())
        if movePool:
            return random.choice(movePool)
            #@todo
            #build decision-tree for 'best' move
        else:
            return False

    def updatePossibleMoves(self):
        possibleMoves = {}
        for moveId, move in self.moves.items():
            if (self.isMovePossible(move)):
                possibleMoves[moveId] = move
        self.possibleMoves=possibleMoves

    def getPossibleMoves(self):
        return self.possibleMoves
        

    def transformCoordinates(self, move):
        """transform x,y to binary"""
        if move in self.moves.keys():
            return self.moves[move]
        else:
            print('move out of range')
            return False


if __name__ == '__main__':
    game = TicTacToe()
    game.mainLoop()
