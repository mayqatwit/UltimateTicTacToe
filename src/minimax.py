import game
import random
# Wrapper to just get move
def minimax(board, depth,maximisingPlayer, scoreFunction):
    col, _ = _minimax(board, depth, maximisingPlayer, scoreFunction)
    return col

def _minimax(game, depth, maximisingPlayer, scoreFunction):
    validLocations = game.getAvailableMoves()

    if len(validLocations) == 0:
        return (None, scoreFunction())
    elif depth == 0:
        return (None, scoreFunction())

    result = game.result
    if result == 0b01:
        return None, float('inf')
    elif result == 0b10:
        return None, float('-inf')
    elif result == 0b11:
        return None, 0

    value = float('-inf') if maximisingPlayer else float('inf')
    best_choice = None

    for board, square in validLocations:
        prev_state = game.state
        game.makeMove(board, square)
        newScore = _minimax(game, depth - 1, not maximisingPlayer, scoreFunction)[1]
        game.undoMove(prev_state)

        if maximisingPlayer and newScore >= value:
            value = newScore
            best_choice = (board, square)
        elif not maximisingPlayer and newScore <= value:
            value = newScore
            best_choice = (board, square)

    return best_choice, value
