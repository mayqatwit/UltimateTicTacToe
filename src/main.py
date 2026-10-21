import termcolor  # Used for colored output

# https://codereview.stackexchange.com/questions/262956/representing-tic-tac-toe-using-a-binary-bitboard

def states_are_equal(state_a, state_b):
    return state_a & state_b == state_b


# Initialize a 32bit value for the board state
STATE   = 0b11100000000000001000000000000000
GAME_ON = 0b10000000000000000000000000000000
PLAYERX = 0b01000000000000000000000000000000
PLAYERO = 0b00100000000000000000000000000000
MASK    = 0b00000000000000001111111111111111
MASKX   = 0b00000011111111100000000000000000
MASKO   = 0b00000000000000000000000111111111
PLAYER  = 0b00000000000000001000000000000000

X_O_BITLEN = 16

# Stores all ways to win when you fill inn a square
ROW1    = 0b0000000000000111
ROW2    = 0b0000000000111000
ROW3    = 0b0000000111000000
COL1    = 0b0000000100100100
COL2    = 0b0000000010010010
COL3    = 0b0000000100100100
DIAG1   = 0b0000000100010001
DIAG2   = 0b0000000001010100

WINNING_ = {
    0b000000001: [ROW1, COL1, DIAG1],
    0b000000010: [ROW1, COL2],
    0b000000100: [ROW1, COL3, DIAG2],
    0b000001000: [ROW2, COL1],
    0b000010000: [ROW2, COL2, DIAG1, DIAG2],
    0b000100000: [ROW2, COL3],
    0b001000000: [ROW3, COL1, DIAG2],
    0b010000000: [ROW3, COL2],
    0b100000000: [ROW3, COL3, DIAG1],
}

# Stores all available squares for the 2**9 possible 3x3 boards
AVAILABLE_MOVES_ = {}
for number in range(2 ** 9):
    bin_str = f"{number:09b}"
    AVAILABLE_MOVES_[number] = sorted(
        8 - index for index, char in enumerate(bin_str) if char == "0"
    )


class BitBoard:
    """
        Simulates a tic tac toe board using a 32 bit integer as state:
    STATE = 0b11100000000000001000000000000000
              1
            The first bit the bit deciding if the game is still active
               1
            The second bit is deciding whose turn it is
               11
            The second and third bit decide whose won after the game is done
            00 = draw, 10 = X won, 01 = O won

    STATE = 0b11100000000000001000000000000000
                            /              /
                       X              O
    """

    def __init__(self, state=None, symbol_X="X", symbol_O="O"):
        self.symbol_X = symbol_X
        self.symbol_O = symbol_O
        self.last_state = None
        self.last_move = None
        self.rows = 3
        self.columns = 3
        self.max_width = 1

        if state:
            self.state = state
        else:
            self.__state = STATE

    def get_available_squares(self):
        return AVAILABLE_MOVES_[(self.__state | self.__state >> X_O_BITLEN) & MASKO]

    def toggle_player(self):
        self.__state ^= PLAYER

    def its_player_Xs_turn(self):
        return self.__state & PLAYER

    def add(self, move):
        if self.its_player_Xs_turn():
            move <<= X_O_BITLEN
        return self.__state | move

    def add_and_update_state(self, move):
        self.last_move = move
        self.last_state = self.__state
        self.state = self.add(move)

    def is_game_over(self):
        return not self.__state & GAME_ON

    def is_move_decisive(self, move):
        state = self.add(move)
        if self.its_player_Xs_turn():
            state >>= X_O_BITLEN
        for win_state in WINNING_[move]:
            if states_are_equal(state, win_state):
                return True
        return False

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state
        if self.is_move_decisive(self.last_move):
            self.__state ^= GAME_ON
            self.__state &= ~(PLAYERX if self.its_player_Xs_turn() else PLAYERO)
        elif not len(self.get_available_squares()):
            self.__state &= ~(GAME_ON | PLAYERX | PLAYERO)
        else:
            self.toggle_player()

    def __repr__(self):
        return bin(self.__state)

    def __str__(self):
        X = termcolor.colored(self.symbol_X, "red", attrs=["bold"])
        O = termcolor.colored(self.symbol_O, "blue", attrs=["bold"])
        border = ""
        sep = " "
        empty = "."
        counter = 0

        column_lst = [empty for _ in range(self.columns)]
        board_matrix = [column_lst for _ in range(self.rows)]
        row_list = []
        for x in range(self.rows):
            for y in range(self.columns):
                mask = 1 << (y + x * self.columns)
                if states_are_equal(self.__state >> X_O_BITLEN, mask):
                    board_matrix[x][y] = f"{X:>{self.max_width}}"
                elif states_are_equal(self.__state, mask):  # mask & self.__state
                    board_matrix[x][y] = f"{O:>{self.max_width}}"
                else:
                    board_matrix[x][y] = f"{counter:>{self.max_width}}"
                counter += 1
            row_list.append(border + sep.join(board_matrix[x][:]) + border)
        return "\n".join(row_list)


if __name__ == "__main__":

    # Just some temp code to show off how the bit board works
    board = BitBoard()
    # print(board, end="\n\n")

    moves = [1, 2, 3, 5, 0, 7, 4, 8]
    moves = [1 << m for m in moves]
    for index in range(len(moves) - 1):
        move, next_move = moves[index], moves[index + 1]
        print("inner.add_and_update_state")
        board.add_and_update_state(move)
        print(board, end="\n")
        print("available squares = ", board.get_available_squares())
        print(
            f"The move {next_move} will{' ' if board.is_move_decisive(next_move) else ' not '}be decisive\n"
        )

    board.add_and_update_state(next_move)
    print(board, end="\n")
    print(board.is_game_over())
