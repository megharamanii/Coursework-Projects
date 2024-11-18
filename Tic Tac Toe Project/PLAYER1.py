import socket
from GAMEBOARD import BoardClass

def connect_to_player2():
    host = input("Enter the host name/IP address of Player 2: ")
    port = input("Enter the port to use: ")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        return sock
    except socket.error as e:
        print(f"Connection failed: {e}")
        return None

def play_again():
    choice = input("Do you want to play again? (y/n): ")
    return choice.lower() == 'y'

def get_player_move(board):
    while True:
        move = input("Enter your move (1-9): ")
        if move.isdigit() and 1 <= int(move) <= 9:
            row = (int(move) - 1) // 3
            col = (int(move) - 1) % 3
            if board[row][col] == ' ':
                return row, col
            else:
                print("Invalid move. Try again.")
        else:
            print("Invalid input. Try again.")

def main():
    board = BoardClass("Player 1")
    sock = connect_to_player2()

    if not sock:
        return

    player2_name = sock.recv(1024).decode()
    print(f"Connected to Player 2: {player2_name}")

    while True:
        board.resetGameBoard()

        while True:
            row, col = get_player_move(board.board)
            board.updateGameBoard(row, col, 'X')
            sock.send(str(row).encode())
            sock.send(str(col).encode())

            if board.isWinner():
                print("Congratulations! You win!")
                board.updateStats('win')
                break
            elif board.boardIsFull():
                print("It's a tie!")
                board.updateStats('tie')
                break

            print("Waiting for Player 2's move...")
            p2_row = int(sock.recv(1024).decode())
            p2_col = int(sock.recv(1024).decode())
            board.updateGameBoard(p2_row, p2_col, 'O')

            if board.isWinner():
                print("Player 2 wins!")
                board.updateStats('loss')
                break

        board.printStats()

        if not play_again():
            break

    sock.send(b"Fun Times")
    sock.close()

if __name__ == '__main__':
    main()
