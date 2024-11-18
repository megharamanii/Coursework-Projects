
class BoardClass:

    def __init__(self,user2):
        """ A simple class to store and handle information about the gameboard. 

       Attributes:
        user1(str) =  Player 1 username
        user2(str) = Player 2 username  
        lastMove(str) = The last player 
        wins(int) = The number of wins 
        ties(int) = The number of ties
        losses(int) = The number of losses
        numGames(int) = The number of games played
        board = The tic tac toe gameboard 
"""
        self.board = [0,0,0,0,0,0,0,0,0]
        self.user1 = "player1"
        self.user2 = user2
        self.lastMove = ""
        self.numGames = 1
        self.wins = {"X": 0, "O": 0}
        self.loss = {"X": 0, "O": 0}
        self.ties = 0


    def updateGamesPlayed(self):
        """Update numGames of the BoardClass.

        Args:
            numGames: The number of games played. 
        """
        self.numGames = self.numGames + 1

    def resetGameBoard(self):
        """Reset the board of the BoardClass.

        Args:
            board: The tic tac toe gameboard 
        """
        self.board = [0,0,0,0,0,0,0,0,0]

    def updateGameBoard(self,position,player):
        """Update positon of the last player from the two users of the BoardClass.

        Args:
            user1: Player 1 username
            user2: Player 2 username  
            board: The tic tac toe gameboard
            lastMove: The last player
        """
        if player == "player1":
            self.board[position] = "O"
            self.lastMove = "player1"
        else:
            self.board[position] = "X"
            self.lastMove = self.user2

    def boardIsFull(self):
        """Check to see if the board is full of the BoardClass.

        Args: 
            board: The tic tac toe gameboard

        Return Bool(True)
        """
        for cell in self.board:
            if cell == 0:
                return False
        
        return True

    def isWinner(self):
        """Check to see the wins/ loss / ties of the BoardClass.

        Args: 
            board: The tic tac toe gameboard
            wins: The number of wins 
            ties: The number of ties
            losses: The number of losses

        Return finish and won 
        """
        finish = False
        won = None
        b1 = self.board[0]
        b2 = self.board[1]
        b3 = self.board[2]
        b4 = self.board[3]
        b5 = self.board[4]
        b6 = self.board[5]
        b7 = self.board[6]
        b8 = self.board[7]
        b9 = self.board[8]

        if (b1==b2 and b1==b3 and b1=="O") or (b4==b5 and b4==b6 and b4=="O") or (b7==b8 and b7==b9 and b7=="O"):
            finish = True
            won = "O"
            self.wins["O"] = self.wins["O"] + 1
            self.loss["X"] = self.loss["X"] + 1
        elif (b1==b2 and b1==b3 and b1=="X") or (b4==b5 and b4==b6 and b4=="X") or (b7==b8 and b7==b9 and b7=="X"):
            finish = True
            won = "X"
            self.wins["X"] = self.wins["X"] + 1
            self.loss["O"] = self.loss["O"] + 1
        elif (b1==b4 and b1==b7 and b1=="O") or (b2==b5 and b2==b8 and b2=="O") or (b3==b6 and b3==b9 and b3=="O"):
            finish = True
            won = "O"
            self.wins["O"] = self.wins["O"] + 1
            self.loss["X"] = self.loss["X"] + 1
        elif (b1==b4 and b1==b7 and b1=="X") or (b2==b5 and b2==b8 and b2=="X") or (b3==b6 and b3==b9 and b3=="X"):
            finish = True
            won = "X"
            self.wins["X"] = self.wins["X"] + 1
            self.loss["O"] = self.loss["O"] + 1
        elif (b1==b5 and b1==b9 and b1=="O") or (b7==b5 and b7==b3 and b7=="O"):
            finish = True
            won = "O"
            self.wins["O"] = self.wins["O"] + 1
            self.loss["X"] = self.loss["X"] + 1
        elif (b1==b5 and b1==b9 and b1=="X") or (b7==b5 and b7==b3 and b7=="X"):
            finish = True
            won = "X"
            self.wins["X"] = self.wins["X"] + 1
            self.loss["O"] = self.loss["O"] + 1
        elif self.boardIsFull():
            finish = True
            self.ties = self.ties + 1

        return finish,won


    def computeStats(self):
        """Compute the statistics of the BoardClass.

        Args: 
            board: The tic tac toe gameboard
            user1: Player 1 username
            user2(:Player 2 username  
            lastMove:The last player 
            wins: The number of wins 
            ties: The number of ties
            losses: The number of losses
            numGames: The number of games played

        Return stats 
    """
        stats = {}
        stats["board"] = self.board
        stats["user1"] = self.user1
        stats["user2"] = self.user2
        stats["lastMove"] = self.lastMove
        stats["numGames"] = self.numGames
        stats["wins"] = self.wins
        stats["loss"] = self.loss
        stats["ties"] = self.ties

        return stats
