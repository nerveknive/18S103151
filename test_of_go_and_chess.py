import numpy as np
import os
from chess_and_go import *

def testPOSITION():
    newGo = Go(1, 2)
    newGo.Board.ShowBoard()
    newGo.Action.Position(1, 1, 4, 4)
    newGo.Board.ShowBoard()

def testMOVE():
    newChess = Chess(1, 2)
    newChess.Board.ShowBoard()
    newChess.Action.MOVE(1, 1, 1, 1, 2)
    newChess.Board.ShowBoard()

def testLIFT():
    newGO = Go(1, 2)
    newGO.Action.Position(1, 1, 2, 3)
    newGO.Action.Position(1, 1, 3, 3)
    newGO.Action.Position(2, 2, 4, 3)
    newGO.Board.ShowBoard()
    newGO.Action.LIFT(2, 2, 3)
    newGO.Board.ShowBoard()


if __name__ == "__main__":
    testPOSITION()
    testMOVE()
    testLIFT()
