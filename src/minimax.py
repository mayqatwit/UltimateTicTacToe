def orderMoves(validLocations, board, piece, maximising, depth, scoreFunction):
    def moveScore(col):
        row = dropPiece(board, col, piece)
        score = scoreFunction(board, piece)
        board[row][col] = 0
        return score
    return sorted(validLocations, key=moveScore, reverse=maximising)

# Wrapper to just get move
def minimax(board, depth, alpha, beta, maximisingPlayer, enemyPiece, scoreFunction, pruning):
    col, _ = _minimax(board, depth, alpha, beta, maximisingPlayer, enemyPiece, scoreFunction, pruning)
    return col

def _minimax(board, depth, alpha, beta, maximisingPlayer, enemyPiece, scoreFunction, pruning):

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

    ordered = orderMoves(validLocations, board, enemyPiece, maximisingPlayer, depth, scoreFunction)
    if maximisingPlayer:
        value = float('-inf')
        column = random.choice(ordered)
        for col in ordered:
            row = dropPiece(board, col, enemyPiece)
            newScore = _minimax(board, depth-1, alpha, beta, False, enemyPiece, scoreFunction, pruning)[1]
            board[row][col] = 0
            if newScore > value:
                value = newScore
                column = col
            if pruning:
                alpha = max(alpha, value)
                if alpha >= beta:
                    return column, value
        result = (column, value, '') if pruning else (column, value)
        return column, value

    else:
        value = float('inf')
        column = random.choice(ordered)
        for col in ordered:
            row = dropPiece(board, col, playerPiece)
            newScore = _minimax(board, depth-1, alpha, beta, True, enemyPiece, scoreFunction, pruning)[1]
            board[row][col] = 0
            if newScore < value:
                value = newScore
                column = col
            if pruning:
                beta = min(beta, value)
                if alpha >= beta:
                    return column, value
        result = (column, value, '') if pruning else (column, value)
        return column, value