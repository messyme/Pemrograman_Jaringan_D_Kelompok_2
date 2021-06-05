import socket
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
import time
import threading
import os


class GUI:

    def __init__(frame, ip_address, port):
        frame.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        frame.server.connect((ip_address, port))

        frame.Window = tk.Tk()
        frame.Window.withdraw()

        frame.login = tk.Toplevel()

        frame.login.title("Welcome Page")
        frame.login.resizable(width=False, height=False)
        frame.login.configure(width=400, height=350)

        frame.pls = tk.Label(frame.login,
                            text="Selamat Datang di Chat Room! \n Silakan Login.",
                            justify=tk.CENTER,
                            font="Arial 12 bold")


        frame.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        frame.userLabelName = tk.Label(frame.login, text="Nama : ", font="Arial 11")
        frame.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        frame.userEntryName = tk.Entry(frame.login, font="Arial 12")
        frame.userEntryName.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.30)
        frame.userEntryName.focus()

        frame.roomLabelName = tk.Label(frame.login, text="Nomor Ruangan : ", font="Arial 12")
        frame.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        frame.roomEntryName = tk.Entry(frame.login, font="Arial 11", show="*")
        frame.roomEntryName.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.45)

        frame.go = tk.Button(frame.login,
                            text="Masuk",
                            font="Arial 12 bold",
                            command=lambda: frame.goAhead(frame.userEntryName.get(), frame.roomEntryName.get()))

        frame.go.place(relx=0.35, rely=0.62)

        frame.Window.mainloop()

    def goAhead(frame, username, room_id=0):
        frame.name = username
        frame.server.send(str.encode(username))
        time.sleep(0.1)
        frame.server.send(str.encode(room_id))

        frame.login.destroy()
        frame.layout()

        rcv = threading.Thread(target=frame.receive)
        rcv.start()

    def layout(frame):
        frame.Window.deiconify()
        frame.Window.title("Chat Room Page")
        frame.Window.resizable(width=False, height=False)
        frame.Window.configure(width=470, height=550, bg="#4472a0")
        frame.chatBoxHead = tk.Label(frame.Window,
                                    bg="#365c87",
                                    fg="#EAECEE",
                                    text=frame.name,
                                    font="Arial 12 bold",
                                    pady=5)

        frame.chatBoxHead.place(relwidth=1)

        frame.line = tk.Label(frame.Window, width=450, bg="#ABB2B9")

        frame.line.place(relwidth=1, rely=0.07, relheight=0.012)

        frame.textCons = tk.Text(frame.Window,
                                width=20,
                                height=2,
                                bg="#ffffff",
                                fg="#000000",
                                font="Arial 12",
                                padx=5,
                                pady=5)

        frame.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
       
        frame.labelBottom = tk.Label(frame.Window, bg="#93b2d1", height=80)

        frame.labelBottom.place(relwidth=1,
                               rely=0.8)

        frame.entryMsg = tk.Entry(frame.labelBottom,
                                 bg="#ffffff",
                                 fg="#000000",
                                 font="Arial 12")

        frame.entryMsg.place(relwidth=0.74,
                            relheight=0.03,
                            rely=0.008,
                            relx=0.011)
        frame.entryMsg.focus()

        frame.buttonMsg = tk.Button(frame.labelBottom,
                                   text="Kirim",
                                   font="Arial 11 bold",
                                   width=20,
                                   bg="#ABB2B9",
                                   command=lambda: frame.sendButton(frame.entryMsg.get()))

        frame.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)

        frame.labelFile = tk.Label(frame.Window, bg="#5d8cba", height=70)

        frame.labelFile.place(relwidth=1,
                             rely=0.9)

        frame.fileLocation = tk.Label(frame.labelFile,
                                     text="Pilih File",
                                     bg="#FFFFFF",
                                     fg="#d2d4d6",
                                     font="Arial 12")
        frame.fileLocation.place(relwidth=0.65,
                                relheight=0.03,
                                rely=0.008,
                                relx=0.011)

        frame.browse = tk.Button(frame.labelFile,
                                text="Cari",
                                font="Arial 11 bold",
                                width=13,
                                bg="#b9abab",
                                command=frame.browseFile)
        frame.browse.place(relx=0.67,
                          rely=0.008,
                          relheight=0.03,
                          relwidth=0.15)

        frame.kirimfileBtn = tk.Button(frame.labelFile,
                                     text="Kirim",
                                     font="Arial 11 bold",
                                     width=13,
                                     bg="#b9abab",
                                     command=frame.sendFile)

        frame.kirimfileBtn.place(relx=0.84,
                               rely=0.008,
                               relheight=0.03,
                               relwidth=0.15)

        frame.textCons.config(cursor="arrow")
        scrollbar = tk.Scrollbar(frame.textCons)
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=frame.textCons.yview)
        frame.textCons.config(state=tk.DISABLED)

    def browseFile(frame):
        frame.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Pilih file",
                                                   filetypes=(("Text files",
                                                               "*.txt*"),
                                                              ("all files",
                                                               "*.*")))
        frame.fileLocation.configure(text="File Dipilih " + frame.filename)

    def sendFile(frame):
        frame.server.send("FILE".encode())
        time.sleep(0.1)
        frame.server.send(str("File " + os.path.basename(frame.filename)).encode())
        time.sleep(0.1)
        frame.server.send(str(os.path.getsize(frame.filename)).encode())
        time.sleep(0.1)

        file = open(frame.filename, "rb")
        data = file.read(1024)
        while data:
            frame.server.send(data)
            data = file.read(1024)
        frame.textCons.config(state=tk.DISABLED)
        frame.textCons.config(state=tk.NORMAL)
        frame.textCons.insert(tk.END, "[ Anda ] "
                             + str(os.path.basename(frame.filename))
                             + " Terkirim\n\n")
        frame.textCons.config(state=tk.DISABLED)
        frame.textCons.see(tk.END)

    def sendButton(frame, msg):
        frame.textCons.config(state=tk.DISABLED)
        frame.msg = msg
        frame.entryMsg.delete(0, tk.END)
        snd = threading.Thread(target=frame.sendMessage)
        snd.start()

    def receive(frame):
        while True:
            try:
                message = frame.server.recv(1024).decode()

                if str(message) == "FILE":
                    file_name = frame.server.recv(1024).decode()
                    lenOfFile = frame.server.recv(1024).decode()
                    send_user = frame.server.recv(1024).decode()

                    if os.path.exists(file_name):
                        os.remove(file_name)

                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = frame.server.recv(1024)
                            total = total + len(data)
                            file.write(data)

                    frame.textCons.config(state=tk.DISABLED)
                    frame.textCons.config(state=tk.NORMAL)
                    frame.textCons.insert(tk.END, "[ " + str(send_user) + " ] " + file_name + " Diterima\n\n")
                    frame.textCons.config(state=tk.DISABLED)
                    frame.textCons.see(tk.END)

                else:
                    frame.textCons.config(state=tk.DISABLED)
                    frame.textCons.config(state=tk.NORMAL)
                    frame.textCons.insert(tk.END,
                                         message + "\n\n")

                    frame.textCons.config(state=tk.DISABLED)
                    frame.textCons.see(tk.END)

            except:
                print("Terdapat error!")
                frame.server.close()
                break

    def sendMessage(frame):
        frame.textCons.config(state=tk.DISABLED)
        while True:
            frame.server.send(frame.msg.encode())
            frame.textCons.config(state=tk.NORMAL)
            frame.textCons.insert(tk.END,
                                 "[ Anda ] " + frame.msg + "\n\n")

            frame.textCons.config(state=tk.DISABLED)
            frame.textCons.see(tk.END)
            break

if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    g = GUI(ip_address, port)