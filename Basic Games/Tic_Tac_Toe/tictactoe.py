# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 14:37:33 2021

@author: Daniel
"""

import sys

BOARD_TEMPLATE = """
  0 1 2
 #_____#
0|{} {} {}|  
1|{} {} {}|  
2|{} {} {}| 
 #_____#"""

BLANK_SPACE = "."
PLAYER_X = "X"
PLAYER_O = "O"
BOARD_WIDTH = 3
BOARD_HEIGHT = 3


def main():
    """Runs a game of Tic-Tac-Toe"""
    game_start = "Tic-Tac-Toe by Daniel Diaz Vigil"
    print(game_start.center(40, "-"))
    gameBoard = getBlankBoard()

    playerTurn = PLAYER_X
    print()
    while True:
        # Shows Game Board
        showBoard(gameBoard)

        # Gets player's move, and updates Dictionary
        playerMove = getPlayerMove(playerTurn, gameBoard)
        gameBoard[(playerMove)] = playerTurn

        # Checks if Winner is found
        if checkWinner(playerTurn, gameBoard):
            showBoard(gameBoard)
            print(f"Congratulations Player {playerTurn}, you have won!")
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
    """ Creates a blank Tic-Tac-Toe board dictionary. """
    board = {}
    for rowIndex in range(BOARD_HEIGHT):
        for columnIndex in range(BOARD_WIDTH):
            board[(columnIndex, rowIndex)] = BLANK_SPACE
    return board


def showBoard(board):
    boardTiles = []
    for rowIndex in range(BOARD_HEIGHT):
        for columnIndex in range(BOARD_WIDTH):
            boardTiles.append(board[(columnIndex, rowIndex)])
    print(BOARD_TEMPLATE.format(*boardTiles))


def getPlayerMove(player, board):
    """Lets player choose a column and row on the board to place their tile."""
    row = "row"
    column = "column"
    while True:
        columnIndex = inputChecker(player, column)
        rowIndex = inputChecker(player, row)
        if board[(columnIndex, rowIndex)] != BLANK_SPACE:
            print(
                "That position is already taken. Pick a position that is not yet taken."
            )
            continue
        if board[(columnIndex, rowIndex)] == BLANK_SPACE:
            return (columnIndex, rowIndex)


def inputChecker(player, axis):
    """Checks if user input is within boards template."""
    while True:
        print(f'{player} enter {axis} number 0-2 or "QUIT" ')
        axisInput = input(">").upper().strip()
        if axisInput == "QUIT":
            sys.exit()
        axisInput = int(axisInput)
        if axisInput in (0, 1, 2):
            return axisInput
        else:
            print("Please enter a position a valid position: 0, 1, or 2")
            continue


def checkFullBoard(board):
    """ Checks if the game board is filled. If so, return True. """
    for columnIndex in range(BOARD_WIDTH):
        for rowIndex in range(BOARD_HEIGHT):
            if board[(columnIndex, rowIndex)] == BLANK_SPACE:
                return False
    return True


def checkWinner(player, board):
    """ Checks if a player has won the game, if so returns True. """
    # Check for Vertical Win
    for column in [0, 1, 2]:
        tile1 = board[(column, 0)]
        tile2 = board[(column, 1)]
        tile3 = board[(column, 2)]
        if tile1 == tile2 == tile3 == player:
            return True
    # Check for Horizontal Win
    for row in [0, 1, 2]:
        tile1 = board[(0, row)]
        tile2 = board[(1, row)]
        tile3 = board[(2, row)]
        if tile1 == tile2 == tile3 == player:
            return True
    # Check for diagonal win left-to-right
    tile1 = board[(0, 0)]
    tile2 = board[(1, 1)]
    tile3 = board[(2, 2)]
    if tile1 == tile2 == tile3 == player:
        return True
    # Checks for diagonal win right-to-left
    tile1 = board[(2, 0)]
    tile2 = board[(1, 1)]
    tile3 = board[(0, 2)]
    if tile1 == tile2 == tile3 == player:
        return True
    return False


if __name__ == "__main__":
    main()
