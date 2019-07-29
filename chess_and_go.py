import numpy as np
import os

class Game:
    #定义Game类
    def __init__(self,type,child,p1,p2):
        self.gtype=type
        self.child=child
        self.p1=p1
        self.p2=p2

    def GetPieceID(self,piece):
        #判断棋子黑白
        if piece==0:
            return
        return piece

    def IsSafePosition(self,x,y):
        #判断落子位置是否合法
        if self.gtype=="chess":
            return not(x<0 or x>7 or y<0 or y>7)
        elif self.gtype=="go":
            return not(x<0 or x>18 or y<0 or y>18)

class Player():
    #定义Player类
    def __init__(self,gtype,playername,piece,playerID):
        self.gtype=gtype
        self.playername=playername
        self.piece=piece
        self.playerID=playerID

class Board(Game):
    #定义棋盘类
    def __init__(self,gtype,p1,p2):
        super(Board,self).__init__(gtype,self,p1,p2)
        if gtype=="chess":
            board=np.zeros((8,8),dtype=object)
            board[0][0]='r1'
            board[0][1]='n1'
            board[0][2]='b1'
            board[0][3]='k1'
            board[0][4]='q1'
            board[0][5]='b1'
            board[0][6]='n1'
            board[0][7]='r1'
            for i in range(8):
                board[1][i]='p1'
            board[7][0]='r2'
            board[7][1]='n2'
            board[7][2]='b2'
            board[7][3]='k2'
            board[7][4]='q2'
            board[7][5]='b2'
            board[7][6]='n2'
            board[7][7]='r2'
            for i in range(8):
                board[6][i]='p1'
            self.board=board
        elif gtype=="go":
            board=np.zeros((19,19),dtype=object)
            self.board=board
            
    def GetPiece(self,x,y):
        #判断棋盘某位置状态
        return self.board[x][y]

    def SetPiece(self,piece,x,y):
        #落子函数
        self.board[x][y]=piece

    def ClearPiece(self,x,y):
        #去子函数
        self.board[x][y]=0

    def ShowBoard(self):
        #显示棋盘
        print(self.board)

class Piece():
    #定义棋子类
    def __init__(self,gtype):
        self.gtype=gtype
        if self.gtype=="go":
            data={'g':19*19}
            self.data=data
        elif self.gtype=="chess":
            data={'k':1,'q':1,'r':2,'b':2,'n':2,'p':8}
            self.data=data
            
class Position():
    #定义棋盘位置类
    def __init__(self,gtype):
        pass

class Action(Game):
    #定义动作类
    def __init__(self,gtype,p1,p2,chess=None,go=None):
        super(Action,self).__init__(gtype,self,p1,p2)
        self.chess=chess
        self.go=go

    def CountPiece(self):
        #计算棋子个数
        if self.gtype=="chess":
            obj=self.chess
        elif self.gtype=="go":
            obj=self.go
        myboard=obj.Board.board
        pl1=pl2=0
        for row in myboard:
            for col in row:
                if 1==self.GetPieceID(col):
                    pl1+=1
                elif 2==self.GetPieceID(col):
                    pl2+=1
        strp1=self.p1+":"+str(pl1)
        strp2=self.p2+":"+str(pl2)
        print(strp1)
        print(strp2)

    def GetPosInfo(self,x,y):
        #判断棋盘某位置信息
        if self.gtype=="chess":
            obj=sef.chess
        elif self.gtype=="go":
            obj=self.go
        if not self.IsSafePosition(x,y):
            return False
        piece=obj.Board.GetPiece(x,y)
        if piece==0:
            print("Empty")
            return
        playerID=int(self.GetPieceID(piece))
        playerobj=obj.GetPlayerbyID(playerID)
        print(piece)
        print(playerobj.playername)

    def Position(self,player,piece,x,y):
        #围棋落子函数
        if self.gtype=="go":
            player=self.go.GetPlayer(player)
            if player.playerID!=self.GetPieceID(piece):
                return False
            if not self.IsSafePosition(x,y):
                return False
            if self.go.Board.GetPiece(x,y)!=0:
                return False
            self.go.Board.SetPiece(piece,x,y)

    def MOVE(self,player,x1,y1,x2,y2):
        #国象走子函数
        if not (self.IsSafePosition(x1,y1) and self.IsSafePosition(x2,y2)):
            return
        if self.chess.Board.GetPiece(x2,y2)!=0:
            return
        if self.chess.Board.GetPiece(x1,y1)==0:
            return
        if x1==x2 and y1==y2:
            return
        playerobj = self.chess.GetPlayer(player)
        piece = self.chess.Board.GetPiece(x1, y1)
        self.chess.Board.SetPiece(piece, x2, y2)
        self.chess.Board.ClearPiece(x1, y1)

    def LIFT(self,player,x,y):
        #围棋提子函数
        if not self.IsSafePosition(x,y):
            return False
        if self.go.Board.GetPiece(x,y)==0:
            return False
        player=self.go.GetPlayer(player)
        piece=self.go.Board.GetPiece(x,y)
        self.go.Board.ClearPiece(x,y)

    def EAT(self,player,x1,y1,x2,y2):
        #吃子函数
        if not(self.IsSafePosition(x1,y1) and self.IsSafePosition(x2,y2)):
            return
        if self.chess.Board.GetPiece(x1,y1)==0:
            return
        if self.chess.Board.GetPiece(x2,y2)==0:
            return
        if x1==x2 and y1==y2:
            return
        player1=self.chess.GetPlayer(player)
        piece1=self.chess.Board.GetPiece(x1,y1)
        piece2=self.chess.Board.GetPiece(x2,y2)
        self.chess.Board.ClearPiece(x2,y2)
        self.chess.Board.SetPiece(piece1,x2,y2)
        self.chess.Board.ClearPiece(x1,y1)
        
class Go(Game):
    #定义围棋类
    def __init__(self,p1,p2):
        super(Go,self).__init__("go",self,p1,p2)
        myBoard=Board(self.gtype,p1,p2)
        self.Board=myBoard
        myPiece1=Piece(self.gtype)
        myPlayer1=Player(self.gtype,p1,myPiece1,1)
        self.player1=myPlayer1
        myPiece2=Piece(self.gtype)
        myPlayer2=Player(self.gtype,p2,myPiece1,2)
        self.player2=myPlayer2
        myAction=Action(self.gtype,p1,p2,go=self)
        self.Action=myAction

    def GetPlayer(self,playername):
        #判断棋手
        if self.player1.playername==playername:
            return self.player1
        elif self.player2.playername==playername:
            return self.player2
        else:
            return

    def GetPlayerbyID(self,ID):
        #判断棋手
        if self.player1.playerID==ID:
            return self.player1
        elif self.player2.playerID==ID:
            return self.player2
        else:
            return

class Chess(Game):
    #定义国象类
    def __init__(self,p1,p2):
        super(Chess,self).__init__("chess",self,p1,p2)
        myBoard=Board(self.gtype,p1,p2)
        self.Board=myBoard
        myPiece1=Piece(self.gtype)
        myPlayer1=Player(self.gtype,p1,myPiece1,1)
        self.player1=myPlayer1
        myPiece2=Piece(self.gtype)
        myPlayer2=Player(self.gtype,p2,myPiece2,2)
        self.player2=myPlayer2
        myAction=Action(self.gtype,p1,p2,chess=self)
        self.Action=myAction

    def GetPlayer(self,playername):
        #判断棋手
        if self.player1.playername==playername:
            return self.player1
        elif self.player2.playername==playername:
            return self.player2
        else:
            return

    def GetPlayerbyID(self,ID):
        #判断棋手
        if self.player1.playerID==ID:
            return self.player1
        elif self.player2.playerID==ID:
            return self.player2
        else:
            return

if __name__=="__main__":
    #主函数
    GameType=input("Game:chess or go:")
    pl1,pl2=input("player1 and player's name:").split(' ')
    if GameType=="chess":
        myGame=Chess(pl1,pl2)
    elif GameType=="go":
        myGame=Go(pl1,pl2)
    i=0
    while True:
        if i%2==0:
            mystr=pl1+"please input:"
            player=pl1
        elif i%2==1:
            mystr=pl2+"please input:"
            player=pl2
        command=input(mystr)
        if command.upper()=="END":
            break
        i+=1
        decomm=command.split(' ')
        if decomm[0].upper() == "EAT":
            myGame.Action.EAT(player, int(decomm[1]), int(decomm[2]), int(decomm[3]), int(decomm[4]))
        elif decomm[0].upper() == "MOVE":
            myGame.Action.MOVE(player, int(decomm[1]), int(decomm[2]), int(decomm[3]), int(decomm[4]))
        elif decomm[0].upper() == "LIFT":
            myGame.Action.LIFT(player, int(decomm[1]), int(decomm[2]))
        elif decomm[0].upper() == "POS":
            myGame.Action.Position(player, int(decomm[1]), int(decomm[2]), int(decomm[3]))
        elif decomm[0].upper() == "INFO":
            myGame.Action.GetPosInfo(int(decomm[1]), int(decomm[2]))
            i -= 1
        elif decomm[0].upper() == "COUNT":
            myGame.Action.CountPiece()
            i -= 1
        else:
            continue
        myGame.Board.ShowBoard()














        
