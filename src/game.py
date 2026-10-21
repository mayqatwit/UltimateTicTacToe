import re

class UltTicTac:
    def __init__(self, state="_________________________________________________________________________________"):
        self.state = state
        self.xWinPattern = "XXX......|...XXX...|......XXX|X..X..X..|.X..X..X.|..X..X..X|X...X...X|..X.X.X.."
        self.oWinPattern = "OOO......|...OOO...|......OOO|O..O..O..|.O..O..O.|..O..O..O|O...O...O|..O.O.O.."

    def boardWin(self, board):
        if len(board) == 9:
            if re.search(self.xWinPattern, board):
                return "X"
            if re.search(self.oWinPattern, board):
                return "O"
            return "_"
        else:
            return None

    def checkWin(self):
        outboard = ""
        for i in range(9):
            subBoard = self.state[i*9:(i+1)*9]
            outboard.append(self.boardWin(subBoard))
        return self.boardWin(outboard)

    def movePos(self, idx):
        subBoard = idx // 9
        subIdx = idx % 9
        boardX = subBoard % 3
        boardY = subBoard // 3
        subX = subIdx % 3
        subY = subIdx // 3

        return (boardX, boardY, subX, subY)

    def moveIdx(self, boardX, boardY, subX, subY):
        return 27*boardY + 9*boardX + 3*subY + subX