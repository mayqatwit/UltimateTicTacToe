import random

import game
import minimax

if __name__ == "__main__":
    game = game.UltimateTicTacToe()
    # simple random game just to see that things are working
    while not game.isGameOver():
        board, square = random.choice(game.getAvailableMoves())
        print(f"{'X' if game.player == 0 else 'O'}: board {board}, square {square}")
        game.makeMove(board, square)
        print(game)
    print(game)
    print("Result:", {0b01: "X wins", 0b10: "O wins", 0b11: "draw"}[game.result])
