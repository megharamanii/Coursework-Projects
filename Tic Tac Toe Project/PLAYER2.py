import socket
from GAMEBOARD import BoardClass

def start_game():
    host = input("Enter your host name/IP address: ")
    port = int(input("Enter the port to use: "))  # Convert input to integer

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))  # Remove the int() conversion from port
    sock.listen(1)
    print("Waiting for Player 1 to connect...")

    conn, addr = sock.accept()
    print("Player 1 connected.")

    return conn

def play_again(choice):
    return choice.lower() == 'y'

def get_player_move(board):
    while True:
        move = input("Enter your move (1-9): ")
        if move.isdigit() and 1 <= int(move) <= 9:
            row = (int(move) - 1) // 3
            col = (int(move) - 1) % 3
            if board.board[row][col] == ' ':  # Access the 'board' attribute of the 'board' object
                return row, col
            else:
                print("Invalid move. Try again.")
        else:
            print("Invalid input. Try again.")

def main():
    board = BoardClass("Player 2")
    conn = start_game()

    player1_name = "Player 1"
    conn.send(player1_name.encode())

    while True:
        board.resetGameBoard()

        while True:
            print("Waiting for Player 1's move...")
            p1_row = int(conn.recv(1024).decode())
            p1_col = int(conn.recv(1024).decode())
            board.updateGameBoard(p1_row, p1_col, 'X')

            if board.isWinner():
                print("Player 1 wins!")
                board.updateStats('loss')
                break
            elif board.boardIsFull():
                print("It's a tie!")
                board.updateStats('tie')
                break

            row, col = get_player_move(board)
            board.updateGameBoard(row, col, 'O')
            conn.send(str(row).encode())
            conn.send(str(col).encode())

            if board.isWinner():
                print("Congratulations! You win!")
                board.updateStats('win')
                break

        board.printStats()

        choice = conn.recv(1024).decode()
        if not play_again(choice):
            break

    conn.close()

if __name__ == '__main__':
    main()
