import random

import game
import minimax
import random
if __name__ == "__main__":
    # game = game.UltimateTicTacToe()
    # # simple random game just to see that things are working
    # while not game.isGameOver():
    #     board, square = random.choice(game.getAvailableMoves())
    #     print(f"{'X' if game.player == 0 else 'O'}: board {board}, square {square}")
    #     game.makeMove(board, square)
    #     print(game)
    #     print(game.h1())
    # print(game)
    # print("Result:", {0b01: "X wins", 0b10: "O wins", 0b11: "draw"}[game.result])
    
    game = game.UltimateTicTacToe()

    while not game.isGameOver():
        is_x = game.player == 0
        func = game.h1
        move = minimax.minimax(game, 4, is_x, func)

        board_index, piece_index = move
        game.makeMove(board_index, piece_index)

        print(f"{"X" if is_x else "O"}: board: {board_index}, square: {piece_index}")
        print(game)


    print(f"Winner of the game was {game.gameWinner}")