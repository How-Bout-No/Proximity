
#=======================================================#
#           P R O X I M I T Y     C H A T               #
#                                                       #
#          ! DO NOT CHANGE VERSION NUMBER !             #
version = '2.0.0'
#=======================================================#

import os
import sys
from tkinter import *
from tkinter import messagebox
import configparser
import time
import threading
from socket import *
from termcolor import *

config = configparser.ConfigParser()
print(os.getcwd())

# Set directories
workdir = os.getcwd()
proxdir = os.path.expanduser('~/AppData/Local/.Proximity')
usrdir = os.path.expanduser('~/Documents/Proximity')
os.chdir(proxdir)
print(os.getcwd())

usr = None


def center(windowmain, windowheight, windowwidth, windowx, windowy):  # Center window
    windowmain.update_idletasks()
    width = windowmain.winfo_width()
    height = windowmain.winfo_height()
    x = (windowmain.winfo_screenwidth() // 2) - (width // 2)
    y = (windowmain.winfo_screenheight() // 2) - (height // 2)
    windowmain.geometry('{}x{}+{}+{}'.format(width - windowwidth, height - windowheight, x - windowx, y - windowy))


def exit_win(main_win):
    main_win.destroy()


def exitinit():
    confirm_exit = messagebox.askyesno(init, message="Are you sure you want to exit?")
    if confirm_exit:
        exit_win(init)
        sys.exit()


######################################################
init = Tk()
init.title("\n")
init.iconbitmap("%s/_files/icon2.ico" % proxdir)

center(init, 100, 0, 0, 0)
init.resizable(False, False)


# init.overrideredirect(True)

def limit_input(*args):
    value = u.get()
    if len(value) > 15: u.set(value[:15])


u = StringVar()
u.trace('w', limit_input)

userlabel = Label(init, text="Username:")
userinput = Entry(init, textvariable=u)


def signin(event=None):
    global usr
    usr = u.get()  # Get username
    f = open("%s/_files/localuser.dat" % proxdir, "a")
    f.write("[user]\n")
    f.write("Username: %s\n" % usr)
    exit_win(init)

login = Button(init, text="Sign In", command=signin)

userlabel.grid(row=1)

userinput.grid(row=1, column=2)

login.grid(columnspan=3)

init.bind('<Return>', signin)

init.protocol('WM_DELETE_WINDOW', exitinit)

if os.path.isfile("%s/_files/localuser.dat" % proxdir):
    config.read("%s/_files/localuser.dat" % proxdir)
    usr = config.get("user", "Username")
    exit_win(init)

init.mainloop()
################################################################################
root = Tk()
root.title("Proximity Chat")
root.iconbitmap(proxdir + "/_files/icon2.ico")


def serverconn():
    global usr
    host_win = Toplevel()
    host_win.title("\n")
    host_win.iconbitmap(proxdir + "/_files/icon2.ico")

    center(host_win, 100, 0, 0, 0)
    host_win.resizable(False, False)

    # init.overrideredirect(True)

    def join_server():
        global ip_out
        global port_out
        ip_out = ip.get()
        port_out = port.get()
        exit_win(host_win)
        establish_conn()

    def limit_input1(*args):
        value = ip.get()
        if len(value) > 20:
            ip.set(value[:20])

    def limit_input2(*args):
        value = port.get()
        if len(value) > 5:
            port.set(value[:5])

    ip = StringVar()
    ip.trace('w', limit_input1)
    port = StringVar()
    port.trace('w', limit_input2)

    iplabel = Label(host_win, text="Server IP:")
    portlabel = Label(host_win, text="Server Port:")
    ipinput = Entry(host_win, textvariable=ip, width=20)
    portinput = Entry(host_win, textvariable=port, width=20)

    ipinput.insert(0, "75.133.121.113")
    portinput.insert(0, "60501")

    join_server = Button(host_win, text="Join Server", command=join_server)

    iplabel.grid(row=1, sticky=W)
    portlabel.grid(row=2, sticky=W)

    ipinput.grid(row=1, column=2, sticky=E)
    portinput.grid(row=2, column=2, sticky=E)

    join_server.grid(columnspan=3)


def server_host():
    global usr
    host_win = Toplevel()
    host_win.title("\n")
    host_win.iconbitmap(proxdir + "/_files/icon2.ico")

    center(host_win, 100, 0, 0, 0)
    host_win.resizable(False, False)

    # init.overrideredirect(True)

    def create_server():
        ipout = ip.get()
        portout = port.get()
        os.chdir(proxdir)
        os.system("start python %s/Server.py %s %s" % (workdir, ipout, portout))
        exit_win(host_win)

    def limit_input(*args):
        value = name.get()
        if len(value) > 30:
            name.set(value[:30])

    def limit_input1(*args):
        value = ip.get()
        if len(value) > 20:
            ip.set(value[:20])

    def limit_input2(*args):
        value = port.get()
        if len(value) > 5:
            port.set(value[:5])

    name = StringVar()
    name.trace('w', limit_input)
    ip = StringVar()
    ip.trace('w', limit_input1)
    port = StringVar()
    port.trace('w', limit_input2)

    namelabel = Label(host_win, text="Server Name:")
    iplabel = Label(host_win, text="Server IP:")
    portlabel = Label(host_win, text="Server Port:")
    nameinput = Entry(host_win, textvariable=name, width=20)
    ipinput = Entry(host_win, textvariable=ip, width=20)
    portinput = Entry(host_win, textvariable=port, width=20)

    nameinput.insert(0, "%s's Server" % usr)
    ipinput.insert(0, "0.0.0.0")
    portinput.insert(0, "60501")

    create_server = Button(host_win, text="Create Server", command=create_server)

    namelabel.grid(row=1, sticky=W)
    iplabel.grid(row=2, sticky=W)
    portlabel.grid(row=3, sticky=W)

    nameinput.grid(row=1, column=2, sticky=E)
    ipinput.grid(row=2, column=2, sticky=E)
    portinput.grid(row=3, column=2, sticky=E)

    create_server.grid(columnspan=3)


def options_win():
    print("Yee")

toolbar = Frame(root)

server = Menubutton(toolbar, text="Server", relief=RAISED)
server.grid()
server.menu = Menu(server, tearoff=0)
server["menu"] = server.menu

Connect = IntVar()
Host = IntVar()

server.menu.add_checkbutton(label="Connect",
                            variable=Connect,
                            command=serverconn)
server.menu.add_checkbutton(label="Host",
                            variable=Host,
                            command=server_host)

server.pack(side=LEFT, padx=2, pady=2)

#options = Menubutton(toolbar, text="Options", relief=RAISED)
#options.menu = Menu(options, tearoff=0)
#options["menu"] = options.menu

#option1 = IntVar()
#option = IntVar()

#options.menu.add_checkbutton(label="Connect", variable=option1)
#options.menu.add_checkbutton(label="Host", variable=option)

#options.pack(side=RIGHT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

Log = Text(root, bg="WHITE", bd=3, height=29, width=122, state=DISABLED)
Log.yview_scroll(1, "units")
Log.pack(pady=5, padx=5, anchor=W)

msgSend = StringVar()
messageSend = Entry(root, bd=3, width=163, textvariable=msgSend)
messageSend.pack(pady=5, padx=5, anchor=W)


def test():
    print("Hello")


# msg = messageSend.trace('w', test)

def establish_conn():
    global messageSend
    global server_address
    Log.config(state=NORMAL)
    sock = socket(AF_INET, SOCK_DGRAM)
    ip = ip_out
    port = int(port_out)
    server_address = (ip, port)
    print(server_address)
    host = gethostbyname(gethostname())
    initip = "<i" + host + "p>"
    cc = "<c" + host + "c>"
    sock.sendto(initip.encode('utf-8'), server_address)
    Log.delete(1.0, END)
    print("Connecting to '%s' port '%s'" % server_address)
    try:
        Log.insert(INSERT, "Connected to '%s' port '%s'\n" % server_address)
        cprint("Connection success!", 'green', attrs=['reverse'])
    except:
        pass
        Log.insert(INSERT, "Connection failed!")
        cprint("Connection failed!", 'red', attrs=['reverse'])

    def get_message():
        #try:
        while True:
            data = sock.recv(512)
            Log.config(state=NORMAL)
            Log.insert(INSERT, "%s\n" % data.decode())
            Log.config(state=DISABLED)
        #except:
            #Log.config(state=NORMAL)
            #Log.insert(INSERT, "Connection to server lost.\n")
            #Log.config(state=DISABLED)
            #cprint("Error! Connection to server lost.", 'red', attrs=['reverse'])

    t = threading.Thread(target=get_message, args=())
    t.daemon = True
    t.start()
    t.setName('getMsg')

    def send_message(var):
        try:
            global messageSend
            message = "%s: %s" % (usr, messageSend.get())
            print(message)
            messageSend.delete(0, END)
            sock.sendto(message.encode('utf-8'), server_address)
        except:
            cprint("Error! Message not sent.", 'red', attrs=['reverse'])

    root.bind("<Return>", send_message)

    def exitroot():
        confirm_exit = messagebox.askyesno(root, message="Are you sure you want to exit?")
        if confirm_exit:
            sock.sendto(cc.encode('utf-8'), server_address)
            exit_win(root)
            sys.exit()

    root.protocol('WM_DELETE_WINDOW', exitroot)

    Log.config(state=DISABLED)


center(root, 0, 0, 0, 0)

root.mainloop()
