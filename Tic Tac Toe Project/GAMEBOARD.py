class BoardClass:
    def __init__(self, player_name):
        self.player_name = player_name
        self.last_player = None
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.games_played = 0
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
#0 1 2
#345
#568 range(0-9)

    def updateGamesPlayed(self):
        self.games_played += 1

    def resetGameBoard(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.last_player = None

    def updateGameBoard(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            self.last_player = player

    def isWinner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True  # Rows
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True  # Columns
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True  # Diagonal
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True  # Diagonal
        return False

    def boardIsFull(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def updateStats(self, result):
        if result == 'win':
            self.wins += 1
        elif result == 'tie':
            self.ties += 1
        elif result == 'loss':
            self.losses += 1

    def printStats(self):
        print(f"Player: {self.player_name}")
        print(f"Last Player: {self.last_player}")
        print(f"Games Played: {self.games_played}")
        print(f"Wins: {self.wins}")
        print(f"Losses: {self.losses}")
        print(f"Ties: {self.ties}")
