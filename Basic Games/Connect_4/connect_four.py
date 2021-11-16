""" Connect-4-Tiles, by Daniel Diaz Vigil danieldiazvigil@gmail.com
A Game where players drop tiles with the aim of connecting 4 tiles in a row.
Similar to Connect Four."""

import sys


PLAYER_X = "X"
PLAYER_O = "O"
BOARD_HEIGHT = 6
BOARD_WIDTH = 7
COLUMN_LABELS = ("1", "2", "3", "4", "5", "6", "7")
BLANK_SPACE = "."

assert len(COLUMN_LABELS) == BOARD_WIDTH

# BOARD TEMPLATE STRING

BOARD_TEMPLATE = """
#_______#
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
#_______#"""


def main():
    """ Runs a game of Connect-4-Tiles."""
    game_start = "Connect-4-Tiles by Daniel Diaz Vigil"
    print(game_start.center(40, "-"))

    # Setting playerTurn
    playerTurn = PLAYER_X

    # Configure New Game:
    gameBoard = getBlankBoard()

    print()

    while True:  # Run a player's turn.
        # Shows current game board
        showBoard(gameBoard)

        # Gets players move
        playerMove = getPlayerMove(playerTurn, gameBoard)

        # Incorporates player move into board
        gameBoard[playerMove] = playerTurn

        if checkWinner(playerTurn, gameBoard):
            showBoard(gameBoard)
            print(f"Congratulations {playerTurn}, you have won!")
            sys.exit()
        elif checkFullBoard(gameBoard):
            showBoard(gameBoard)
            print("The board has filled up and no one has won. It's a Tie!")
            print("Play again? (Y/N):")
            while True:
                playagain = input(">").upper().strip()
                if playagain == "Y":
                    main()
                elif playagain == "N":
                    sys.exit()
                else:
                    print("Please enter either 'Y', or 'N'")
                    continue
        # Switch move to other player:
        if playerTurn == PLAYER_X:
            playerTurn = PLAYER_O
        elif playerTurn == PLAYER_O:
            playerTurn = PLAYER_X


def getBlankBoard():
    """ Returns dictionary that represents blank game board"""
    board = {}
    for rowIndex in range(BOARD_HEIGHT):
        for columnIndex in range(BOARD_WIDTH):
            board[(columnIndex, rowIndex)] = BLANK_SPACE
    return board


def showBoard(board):
    """ Shows properly formatted game board to players. """
    tiles = []
    for rowIndex in range(BOARD_HEIGHT):
        for columnIndex in range(BOARD_WIDTH):
            # Each list value mapped to corresponding dict tuple (row, column)
            tiles.append(board[(columnIndex, rowIndex)])
    print(BOARD_TEMPLATE.format(*tiles))  # Fills in {} with tiles list


def getPlayerMove(player, board):
    """Lets player choose a column on the board to drop a tile into. """
    # Returns a tuple of the (column, row) the tile will land

    while True:  # While loop till valid move played
        print(f"Player {player}, enter 1 to {BOARD_WIDTH} or QUIT:")
        response = input(">").upper().strip()

        if response == "QUIT":
            print("Thank you for playing!")
            sys.exit()
        if response not in COLUMN_LABELS:
            print(f"Enter a number from 1 to {BOARD_WIDTH}.")
            continue  # Restart while loop; ask for move again.
        columnIndex = int(response) - 1  # Accounting for python 0-indexing.

        if board[(columnIndex, 0)] != BLANK_SPACE:
            print("That column is filled, select another one.")
            continue
        # Find first empty row in user-picked column.
        # For loop accounts for 0-indexing. Starts at highest-index row.
        # highest-index row is actually lowest row in displayed to user.
        # -1 steps, till empty space is found
        for rowIndex in range(BOARD_HEIGHT - 1, -1, -1):
            if board[(columnIndex, rowIndex)] == BLANK_SPACE:
                return (columnIndex, rowIndex)


def checkFullBoard(board):
    """ Checks if the game board is full, returns TIE if full and no winner."""
    # Since tiles will fill bottom to top, if all tiles with rowIndex == 0
    # are filled, all tiles below will be filled as well.
    for columnIndex in range(BOARD_WIDTH):
        if board[(columnIndex, 0)] == BLANK_SPACE:
            return False  # Blank space found, return False.
    return True  # All spaces are filled, return True.


def checkWinner(player, board):
    """ Checks if there are 4 matching tiles in a row and if so, returns True."""
    # Iterate through entire board, checking for four tiles in-a-row.

    # -3 ensure that we do not receive a KeyError and that we are operating in-
    # board parameter.
    for columnIndex in range(BOARD_WIDTH - 3):
        for rowIndex in range(BOARD_HEIGHT):
            # Checks for horizontal 4-in-a-row; left-to-right(column).
            tile1 = board[(columnIndex, rowIndex)]
            tile2 = board[(columnIndex + 1, rowIndex)]
            tile3 = board[(columnIndex + 2, rowIndex)]
            tile4 = board[(columnIndex + 3, rowIndex)]
            if tile1 == tile2 == tile3 == tile4 == player:
                return True
    for columnIndex in range(BOARD_WIDTH):
        for rowIndex in range(BOARD_HEIGHT - 3):
            # Checks for vertical 4-in-a-row; top-down (rows).
            tile1 = board[(columnIndex, rowIndex)]
            tile2 = board[(columnIndex, rowIndex + 1)]
            tile3 = board[(columnIndex, rowIndex + 2)]
            tile4 = board[(columnIndex, rowIndex + 3)]
            if tile1 == tile2 == tile3 == tile4 == player:
                return True
    for columnIndex in range(BOARD_WIDTH - 3):
        for rowIndex in range(BOARD_HEIGHT - 3):
            # Checks for diagonal 4-in-a-row, T1, T2 = RIGHT 1, DOWN 1, respective to T1.
            tile1 = board[(columnIndex, rowIndex)]
            tile2 = board[(columnIndex + 1, rowIndex + 1)]
            tile3 = board[(columnIndex + 2, rowIndex + 2)]
            tile4 = board[(columnIndex + 3, rowIndex + 3)]
            if tile1 == tile2 == tile3 == tile4 == player:
                return True
    return False


if __name__ == "__main__":
    main()
