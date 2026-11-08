import random
# https://codereview.stackexchange.com/questions/262956/representing-tic-tac-toe-using-a-binary-bitboard 
OPEN, X_WIN, O_WIN, DRAW = 0b00, 0b01, 0b10, 0b11 # board is open, X wins, O wins, or draw
X, O = 0b0, 0b1 # player ids
ANY_BOARD = 9 # required board bit representation if player can play anywhere

FULL = 0b111111111
WIN_LINES = (
    0b000000111, 0b000111000, 0b111000000, # rows
    0b001001001, 0b010010010, 0b100100100, # columns
    0b100010001, 0b001010100, # diagonals
)

# bits 0-161: nine boards x two 9-bit piece masks (X then O)
# bits 162-179: nine 2-bit board results (OPEN, X_WIN, O_WIN, DRAW)
# bits 180-183: required board (9 = any)
# bit 184: player to move
# bits 185-186: game result
RESULTS_SHIFT = 162
REQUIRED_BOARD_SHIFT = 180
PLAYER_SHIFT = 184
RESULT_SHIFT =185

def hasWin(pieces):
    return any(pieces & line == line for line in WIN_LINES)

class UltimateTicTacToe:
    def __init__(self):
        self.state = ANY_BOARD << REQUIRED_BOARD_SHIFT

    def _get(self, shift, width):
        # get width number of bits starting at shift from the state
        return (self.state >> shift) & ((1 << width) - 1)

    def _set(self, shift, width, value):
        # set width number of bits starting at shift in the state to value
        mask = (1 << width) - 1
        self.state = (self.state & ~(mask << shift)) | (value << shift)

    @property
    def player(self):
        return self._get(PLAYER_SHIFT, 1)

    @property
    def result(self):
        return self._get(RESULT_SHIFT, 2)

    @property
    def requiredBoard(self):
        value = self._get(REQUIRED_BOARD_SHIFT, 4)
        return None if value == ANY_BOARD else value

    def pieces(self, board, player):
        # the given players pieces on the given board
        return self._get(9 * (2 * board + player), 9)

    def occupied(self, board):
        # all occupied spaces
        return self.pieces(board, X) | self.pieces(board, O)

    def boardResult(self, board):
        # the result of a given board (OPEN, X_WIN, O_WIN, DRAW)
        return self._get(RESULTS_SHIFT + 2 * board, 2)

    def isGameOver(self):
        return self.result != OPEN

    def getAvailableMoves(self):
        # game is over, no moves available
        if self.isGameOver():
            return []

        # either the player has a required board to play in or they can play in any open board
        if self.requiredBoard is not None:
            boards = [self.requiredBoard]
        else:
            boards = [board for board in range(9) if self.boardResult(board) == OPEN]

        # return all available moves in the required board(s)
        return [(board, square) for board in boards for square in range(9)
                if not (self.occupied(board) >> square) & 1]

    def makeMove(self, board, square):
        previous = self.state
        player = self.player
        updatedBoard = self.pieces(board, player) | (1 << square) # add the move to the player's pieces bits
        self._set(9 * (2 * board + player), 9, updatedBoard) # and set the new bits to the state 

        if hasWin(updatedBoard): # this board is won
            self._set(RESULTS_SHIFT + 2 * board, 2, player + 1)
        elif self.occupied(board) == FULL: # the board is full but no winner
            self._set(RESULTS_SHIFT + 2 * board, 2, DRAW)

        results = [self.boardResult(i) for i in range(9)]
        won = sum(1 << i for i, result in enumerate(results) if result == player + 1)

        if hasWin(won): # the player won the game
            self._set(RESULT_SHIFT, 2, player + 1)
        elif OPEN not in results: # all boards done and no winner
            self._set(RESULT_SHIFT, 2, DRAW)

        # if the board in the position the player played in is open, send the next player there otherwise they can play anywhere
        if results[square] == OPEN:
            nextBoard = square
        else:
            nextBoard = ANY_BOARD

        self._set(REQUIRED_BOARD_SHIFT, 4, nextBoard) # set the next board bits
        self.state ^= 1 << PLAYER_SHIFT # switch players
        return previous

    def undoMove(self, previous):
        self.state = previous

    def __str__(self):
        rows = []
        for bigRow in range(3):
            for row in range(3):
                parts = []
                for big_col in range(3):
                    board = bigRow * 3 + big_col
                    cells = []
                    for col in range(3):
                        bit = 1 << (row * 3 + col)
                        cells.append("X" if self.pieces(board, X) & bit else "O" if self.pieces(board, O) & bit else ".")
                    parts.append(" ".join(cells))
                rows.append(" | ".join(parts))
            if bigRow < 2:
                rows.append("------+-------+------")
        return "\n".join(rows) + "\n"
