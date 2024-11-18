import socket
import threading
import GAMEBOARD1 as gb
from tkinter import *
from tkinter import messagebox

host = '127.0.0.1'
port = 3000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)

clientSocket, clientAddress = None, None
start = False
user = False
player2 = ""
board = None
state = 0
end = False

def createThread(cnt):
    thread = threading.Thread(target=cnt)
    thread.daemon = True
    thread.start()

def receive():
    global start, user, player2, board
    while True:
        if start and not user:
            try:
                data, addr = clientSocket.recvfrom(1024)
                name = data.decode()
                print(data)
                board = gb.Board(name)
                player2 = name
                sendData = '{}'.format("player1").encode()
                clientSocket.send(sendData)
                user = True
            except:
                pass

def receiveMove():
    global state, start
    while True:
        if start and user:
            try:
                data, addr = clientSocket.recvfrom(1024)
                data = data.decode()
                print(data)
                if data == "Play Again":
                    reset()
                elif data == "Fun Times":
                    gameOver()
                else:
                    state, board.lastMove = data.split("-")
                    board.playMoveOnBoard(int(state), board.lastMove)
                    updateBoard()
                    lblTurn["text"] = "You"
                    play()
            except:
                pass

def acceptConnection():
    print("Thread created")
    global clientSocket, clientAddress, start
    clientSocket, clientAddress = serverSocket.accept()
    message = "Incoming play request from " + str(clientAddress) + " client?"
    answer = messagebox.askyesno("Question", message)
    if answer:
        sendData = '{}'.format("accepted").encode()
        clientSocket.send(sendData)
        start = True
        reset()
        resetStat()
        print(sendData)
        print("Client connected from: ", clientAddress)
        receive()
    else:
        sendData = '{}'.format("Not accepted").encode()
        clientSocket.send(sendData)
        clientSocket.close()
        print("Client socket closes")

def clickQuit():
    if start or user:
        serverSocket.close()
    window.destroy()

createThread(acceptConnection)
createThread(receiveMove)

window = Tk()
window.title("Tic Tac Toe")
window.geometry("500x500")
window.configure(background='White')

mainFrame = Frame(window, bg='White', pady=10)
mainFrame.pack()

lblTitle = Label(mainFrame, text="Tic Tac Toe Game", font=('Arial', 24), bg='White')
lblTitle.pack()

gameFrame = Frame(mainFrame, bg='White')
gameFrame.pack()

btnFrame = Frame(mainFrame, bg='White')
btnFrame.pack()

def playMove(index):
    global end, board
    if start and user and buttons[index].cget("text") == " ":
        if board.lastMove == player2:
            buttons[index].config(text="O")
            board.lastMove = "player1"
            sendData = '{}-{}'.format(index, board.lastMove).encode()
            clientSocket.send(sendData)
            board.playMoveOnBoard(index, board.lastMove)
            lblTurn["text"] = f"opponent: {player2}"
            print(sendData)
            play()

buttons = []
for i in range(9):
    button = Button(gameFrame, text=" ", bg="LightGray", fg="Black", width=6, height=3,
                    font=('Arial', 20), command=lambda index=i: playMove(index))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

btnQuit = Button(btnFrame, text="Quit", font=('Arial', 14), height=1, width=10, command=clickQuit)
btnQuit.pack()

lblStats = Label(btnFrame, font=('Arial', 14), bg="White")
lblStats.pack()

def updateStats(comData):
    lblStats["text"] = f"Games: {comData['numGames']}\nWon: {comData['wins']['O']}\nLost: {comData['loss']['O']}\nTies: {comData['ties']}"

def updateBoard():
    global state
    buttons[int(state)].config(text="X")

def play():
    end, won = board.isGameFinished()
    if end:
        board.recordGamePlayed()
        board.resetGameBoard()
        board.lastMove = "player1"
        comData = board.computeStats()
        updateStats(comData)
        

def gameOver():
    isCon = False
    start = False
    user = False
    close = True
    clientSocket.close()
    board.numGames = board.numGames - 1
    comData = board.computeStats()
    updateStats(comData)
    lblTurn["text"] = f"opponent: {player2}"
    reset()

def reset():
    for button in buttons:
        button.config(text=" ")

def resetStat():
    lblTurn["text"] = f"opponent: {player2}"
    updateStats({'numGames': '', 'wins': {'O': ''}, 'loss': {'O': ''}, 'ties': ''})

lblTurn = Label(mainFrame, text="opponent's turn", font=('Arial', 16), bg='White', pady=10)
lblTurn.pack()

window.mainloop()
