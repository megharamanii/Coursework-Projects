# Import the sockets library
import socket
import threading
import GAMEBOARD1 as gb

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

# Define my socket address information
host = None
port2 = None

# Create a socket object on my server
conn = None

start = False
user = False
player1 = ""
board = None
state = 0
end = False
username = ""
isCon = False
close = False

def createThread(cnt):
    thread = threading.Thread(target=cnt)
    thread.daemon = True
    thread.start()


def receiveMove():
    global state, start, user
    while True:
        if isCon and start and user:
            try:
                data, addr = conn.recvfrom(1024)
                data = data.decode()
                print(data)
                if data != "":
                    state, board.lastMove = data.split("-")
                    board.updateGameBoard(int(state), board.lastMove)
                    updateBoard()
                    lblTurn["text"] = "You"
                    play()
            except:
                lblTurn["text"] = "you"
                pass


def receive():
    global start, user, board, username, player1, conn, isCon, close
    while True:
        if isCon:
            if (not start or not user):
                data, addr = conn.recvfrom(1024)
                data = data.decode()
                print(data)
                if data == "Not accepted":
                    isCon = True
                    conn.close()
                elif data == "accepted":
                    username = simpledialog.askstring("Input", "Enter your name?", parent=window)
                    # username = "maneesha"
                    sendData = '{}'.format(username).encode()
                    conn.send(sendData)
                    lblUsername["text"] = username
                    print(sendData)
                    start = True
                    close = False
                elif data == "player1":
                    player1 = data
                    board = gb.Board(username)
                    board.lastMove = player1
                    user = True
                    break


def clickConnect():
    global host, port2, conn, isCon
    if not isCon:
        host = simpledialog.askstring("Input", "What is host name/ip address?", parent=window)
        port2 = simpledialog.askstring("Input", "What is the port?", parent=window)
        if host != "" and port2 != "":
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((host, int(port2)))
                isCon = True
                lblTurn["text"] = "You"
                lblGames["text"] = " "
                lblWon["text"] = " "
                lblLost["text"] = " "
                lblTies["text"] = " "
                lblUsername["text"] = " "
                try:
                    receive()
                except Exception:
                    isCon = False
                    messagebox.showerror("Error", "Host rejected to connect!")
            except Exception:
                messagebox.showerror("Error", "Invalid hostname or port!")
        else:
            messagebox.showerror("Error", "Invalid hostname or port!")


def clickQuit():
    if start or user:
        conn.close()
    window.destroy()


createThread(receiveMove)


window = Tk()
window.title("TiC-Tac-Toe Player2")
window.geometry("930x650+0+0")
window.resizable(width=False, height=False)
window.configure(background='white smoke')

tops = Frame(window, bg='white smoke', pady=2, width=1350, height=100, relief=RIDGE)
tops.grid(row=0, column=0)

lblTitle = Label(tops, font=('arial', 50, 'bold'), text="Tic Tac Toe Game", bd=21, bg='white smoke', fg='black',
                 justify=CENTER)
lblTitle.grid(row=0, column=0)

mainFrame = Frame(window, bg='gainsboro', bd=10, width=1350, height=600, relief=RIDGE)
mainFrame.grid(row=1, column=0)

leftFrame = Frame(mainFrame, bd=10, width=750, height=500, pady=2, padx=10, bg="gainsboro", relief=RIDGE)
leftFrame.pack(side=LEFT)

rightFrame = Frame(mainFrame, bd=10, width=560, height=500, padx=10, pady=2, bg="gainsboro", relief=RIDGE)
rightFrame.pack(side=RIGHT)

rightFrame1 = Frame(rightFrame, bd=10, width=560, height=200, padx=10, pady=2, bg="gainsboro", relief=RIDGE)
rightFrame1.grid(row=0, column=0)

rightFrame2 = Frame(rightFrame, bd=10, width=560, height=250, padx=10, pady=2, bg="gainsboro", relief=RIDGE)
rightFrame2.grid(row=1, column=0)

rightFrame3 = Frame(rightFrame, bd=10, width=560, height=150, padx=10, pady=2, bg="gainsboro", relief=RIDGE)
rightFrame3.grid(row=2, column=0)


def clicked(index):
    global end, board
    if start and user and btns[index]["text"] == " ":
        if board.lastMove == player1:
            btns[index]["text"] = "X"
            board.lastMove = username
            sendData = '{}-{}'.format(index, board.lastMove).encode()
            conn.send(sendData)
            board.updateGameBoard(index, board.lastMove)
            lblTurn["text"] = "opponent"
            print(sendData)
            play()


def play():
    global isCon, start, user, close
    end, won = board.isWinner()
    if end:
        if won == "O":
            messagebox.showinfo(title=None, message=f"{player1} WON!")
        elif won == "X":
            messagebox.showinfo(title=None, message=f"{username} WON!")
        answer = messagebox.askyesno("Question", "Do you want to play again?")
        if answer:
            sendData = '{}'.format("Play Again").encode()
            conn.send(sendData)
            board.updateGamesPlayed()
            reset()
            comData = board.computeStats()
            lblGames["text"] = comData["numGames"] - 1
            lblWon["text"] = comData["wins"]["X"]
            lblLost["text"] = comData["loss"]["X"]
            lblTies["text"] = comData["ties"]
        else:
            isCon = False
            sendData = '{}'.format("Fun Times").encode()
            conn.send(sendData)
            conn.close()
            start = False
            user = False
            close = True
            comData = board.computeStats()
            lblGames["text"] = comData["numGames"]
            lblWon["text"] = comData["wins"]["X"]
            lblLost["text"] = comData["loss"]["X"]
            lblTies["text"] = comData["ties"]
            lblTurn["text"] = "You"
            reset()


def reset():
    board.resetGameBoard()
    board.lastMove = player1
    for btn in btns:
        btn["text"] = " "


def updateBoard():
    if int(state) in range(9):
        btns[int(state)]["text"] = "O"


btns = []
for i in range(9):
    btn = Button(leftFrame, text=" ", bg="light gray", fg="black", width=8, height=3, font=('Times', 26),
                 command=lambda index=i: clicked(index))
    btn.grid(column=(i % 3) + 1, row=(i // 3) + 1, sticky=S + N + E + W)
    btns.append(btn)

btnConnect = Button(rightFrame3, text="Connect", font=('arial', 17, 'bold'), height=1, width=20, command=clickConnect)
btnConnect.grid(row=2, column=0, padx=6, pady=11)

btnQuit = Button(rightFrame3, text="Quit", font=('arial', 17, 'bold'), height=1, width=20, command=clickQuit)
btnQuit.grid(row=3, column=0, padx=6, pady=10)

lbl = Label(rightFrame2, font=('arial', 20, 'bold'), text="Games:", padx=2, pady=2, bg="gainsboro")
lbl.grid(row=0, column=0, sticky=W)
lblGames = Label(rightFrame2, font=('arial', 20, 'bold'), text=" ", padx=2, pady=2, bg="gainsboro", width=10)
lblGames.grid(row=0, column=1, sticky=W)
lbl = Label(rightFrame2, font=('arial', 20, 'bold'), text="Won:", padx=2, pady=2, bg="gainsboro")
lbl.grid(row=1, column=0, sticky=W)
lblWon = Label(rightFrame2, font=('arial', 20, 'bold'), text=" ", padx=2, pady=2, bg="gainsboro", width=10)
lblWon.grid(row=1, column=1, sticky=W)
lbl = Label(rightFrame2, font=('arial', 20, 'bold'), text="Lost:", padx=2, pady=2, bg="gainsboro")
lbl.grid(row=2, column=0, sticky=W)
lblLost = Label(rightFrame2, font=('arial', 20, 'bold'), text=" ", padx=2, pady=2, bg="gainsboro", width=10)
lblLost.grid(row=2, column=1, sticky=W)
lbl = Label(rightFrame2, font=('arial', 20, 'bold'), text="Ties:", padx=2, pady=2, bg="gainsboro")
lbl.grid(row=3, column=0, sticky=W)
lblTies = Label(rightFrame2, font=('arial', 20, 'bold'), text=" ", padx=2, pady=2, bg="gainsboro", width=10)
lblTies.grid(row=3, column=1, sticky=W)

lbl = Label(rightFrame1, font=('arial', 20, 'bold'), text="Player2:", padx=2, pady=2, bg="gainsboro")
lbl.grid(row=0, column=0, sticky=W)
lblUsername = Label(rightFrame1, font=('arial', 20, 'bold'), text="", padx=2, pady=2, bg="gainsboro", width=10)
lblUsername.grid(row=0, column=1, sticky=W)
lbl = Label(rightFrame1, font=('arial', 20, 'bold'), text="Turn: ", padx=2, pady=2, bg="gainsboro")
lbl.grid(row=1, column=0, sticky=W)
lblTurn = Label(rightFrame1, font=('arial', 20, 'bold'), text="You", padx=2, pady=2, bg="gainsboro", width=10)
lblTurn.grid(row=1, column=1, sticky=W)


window.mainloop()
