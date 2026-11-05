# Wrapper to just get move
def minimax(board, depth,maximisingPlayer, enemyPiece, scoreFunction):
    col, _ = _minimax(board, depth, maximisingPlayer, enemyPiece, scoreFunction)
    return col

def _minimax(board, depth, maximisingPlayer, enemyPiece, scoreFunction):

    validLocations = getValidLocations(board)
    playerPiece = 1 if enemyPiece == 2 else 2

    if len(validLocations) == 0:
        return (None, 0)
    elif depth == 0:
        return (None, scoreFunction(board, enemyPiece))
    elif game.checkWin(board, enemyPiece):
        return (None, float('inf'))
    elif game.checkWin(board, playerPiece):
        return (None, float('-inf'))

    if maximisingPlayer:
        value = float('-inf')
        column = random.choice(validLocations)
        for col in ordered:
            row = dropPiece(board, col, enemyPiece)
            newScore = _minimax(board, depth-1, False, enemyPiece, scoreFunction)[1]
            board[row][col] = 0
            if newScore > value:
                value = newScore
                column = col

        return column, value

    else:
        value = float('inf')
        column = random.choice(validLocations)
        for col in ordered:
            row = dropPiece(board, col, playerPiece)
            newScore = _minimax(board, depth-1, True, enemyPiece, scoreFunction)[1]
            board[row][col] = 0
            if newScore < value:
                value = newScore
                column = col
        return column, value
