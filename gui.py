import configparser
import json
import pickle
import threading
import traceback
import winsound
from base64 import b64encode
from hashlib import sha256
from shutil import copyfile
from socket import *
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from urllib.request import *

from termcolor import *
from win10toast import ToastNotifier

from _files import img

toaster = ToastNotifier()
config = configparser.ConfigParser()
ProximityVersion = "2.3.0"
# Set directories
workdir = os.getcwd()
print(os.getcwd())


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


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

update1 = Tk()
update1.title("\n")
update1.iconbitmap(resource_path("_files\\icon.ico"))

center(update1, 80, 40, 0, 0)
update1.resizable(False, False)

# init.overrideredirect(True)

updategif = resource_path("_files\\_update.gif")
downloadgif = resource_path("_files\\_download.gif")

framecount = 30

framesupdate = [PhotoImage(file=updategif, format='gif -index %i' % (i)) for i in range(framecount)]
framesdownload = [PhotoImage(file=downloadgif, format='gif -index %i' % (i)) for i in range(framecount)]


def updateapp():
    global setting, donevar
    try:
        if not len(sys.argv) > 1:
            r = urlopen("https://api.github.com/repos/How-Bout-No/Proximity/releases/latest")
            data = r.read()
            encoding = r.info().get_content_charset('utf-8')
            JSON_object = json.loads(data.decode(encoding))
            if ProximityVersion < JSON_object['tag_name']:
                setting = 1
                if not os.path.isfile(JSON_object['assets'][0]['name']):
                    urlretrieve(JSON_object['assets'][0]['browser_download_url'], JSON_object['assets'][0]['name'])

                arg1 = b64encode(json.dumps(JSON_object).encode('utf-8')).decode('utf-8')

                copyfile(resource_path("_files\\Updater.exe"), "./Updater.exe")
                os.system(f"start Updater.exe {arg1}")
                sys.exit()
            else:
                donevar = [True, True, False]
        else:
            if os.path.isfile("Updater.exe"):
                os.remove("Updater.exe")
            donevar = [True, True, False]
    except:
        donevar = [True, False, None]


donevar = [False, None, None]
setting = 0
counter = 1


def update(ind):
    global counter, setting, donevar, t
    ind = ind % framecount
    if setting == 0:
        frame = framesupdate[ind]
    elif setting == 1:
        message.config(text="Downloading update...")
        frame = framesdownload[ind]
    ind += 1
    label.configure(image=frame)
    update1.after(framecount, update, ind)
    try:
        if (counter > 10) or (counter == 0):
            try:
                t.isAlive()
            except NameError:
                counter = 0
                t = threading.Thread(target=updateapp, args=())
                t.daemon = True
                t.start()
                t.setName('checkforupdates')
            finally:
                if donevar[0] == True:
                    if donevar[1] == True:
                        if donevar[2] == True:
                            donevar = [None, None, None]
                            messagebox.showinfo(update1, message="Update success!")
                        exit_win(update1)
                    elif donevar[1] == False:
                        donevar = [None, None, None]
                        messagebox.showinfo(update1, message="Update failed!")
                        exit_win(update1)
                        sys.exit()

    except NameError:
        pass
    finally:
        if not counter == 0:
            counter += 1


helv = Font(family="Helvetica", size="10")
message = Label(update1, text="Checking for updates...", font=helv)
label = Label(update1)
message.pack()
label.pack(expand=YES, fill=BOTH)

update1.after(0, update, 0)

update1.mainloop()

######################################################
init = Tk()
init.title("\n")

center(init, 100, 0, 0, 0)
init.resizable(False, False)
init.iconbitmap(resource_path("_files\\icon.ico"))


# init.overrideredirect(True)

def limit_input(*args):
    value = u.get()
    if len(value) > 15: u.set(value[:15])


u = StringVar()
u.trace('w', limit_input)
p = StringVar()
c = StringVar()
q = StringVar()

userlabel = Label(init, text="Username:")
userinput = Entry(init, textvariable=u)
passlabel = Label(init, text="Password:")
passinput = Entry(init, show="•", textvariable=p)


def signin(event=None):
    global usr
    donevar = False
    usr = u.get()  # Get username
    pswrd = p.get()  # Get password
    if (usr == "" or pswrd == "" or " " in usr or " " in pswrd):
        messagebox.showerror(init, message="Invalid Username/Password")
    else:
        if os.path.isdir(workdir + "\\profile") and os.path.isfile(workdir + "\\profile\\localuser.dat") and (
                os.stat(workdir + "\\profile\\localuser.dat").st_size != 0):
            config.read(workdir + "\\profile\\localuser.dat")
            for acc in config.sections():
                if sha256(usr.encode('utf-8')).hexdigest() == config.get(acc, "Username"):
                    if sha256(pswrd.encode('utf-8')).hexdigest() == config.get(acc, "Password"):
                        donevar = True
                        exit_win(init)
                    else:
                        messagebox.showerror(init, message="Incorrect Password")
                        passinput.delete(0, END)
                        donevar = True
            if donevar == False:
                if messagebox.askquestion(init,
                                          message=f"User '{usr}' does not exist.\nWould you like to create a new profile?") == "yes":
                    if not os.path.isdir(workdir + "\\profile"):
                        os.mkdir(workdir + "\\profile")
                    if not os.path.isfile(workdir + "\\profile\\localuser.dat"):
                        f = open(workdir + "\\profile\\localuser.dat", "w+")
                        f.close()
                    config.read(workdir + "\\profile\\localuser.dat")
                    counter = 1
                    while str(counter) in config.sections():
                        counter += 1
                    config[str(counter)] = {'Username': sha256(usr.encode('utf-8')).hexdigest(),
                                            'Password': sha256(pswrd.encode('utf-8')).hexdigest()}
                    with open(workdir + "\\profile\\localuser.dat", 'w') as configfile:
                        config.write(configfile)
                    exit_win(init)
        else:
            if messagebox.askquestion(init,
                                      message=f"User '{usr}' does not exist.\nWould you like to create a new profile?") == "yes":
                if not os.path.isdir(workdir + "\\profile"):
                    os.mkdir(workdir + "\\profile")
                if not os.path.isfile(workdir + "\\profile\\localuser.dat"):
                    f = open(workdir + "\\profile\\localuser.dat", "w+")
                    f.close()
                config.read(workdir + "\\profile\\localuser.dat")
                counter = 1
                while str(counter) in config.sections():
                    counter += 1
                config[str(counter)] = {'Username': sha256(usr.encode('utf-8')).hexdigest(),
                                        'Password': sha256(pswrd.encode('utf-8')).hexdigest()}
                with open(workdir + "\\profile\\localuser.dat", 'w') as configfile:
                    config.write(configfile)
                exit_win(init)
    """
    f = open("%s./_files/localuser.dat" % workdir, "a")
    f.write("[user]\n")
    f.write("Username: %s\n" % usr)
    exit_win(init)
    """


login = Button(init, text="Sign In", command=signin)

userlabel.grid(row=1)
passlabel.grid(row=2)

userinput.grid(row=1, column=2)
passinput.grid(row=2, column=2)

login.grid(columnspan=3)

init.bind('<Return>', signin)

init.protocol('WM_DELETE_WINDOW', exitinit)

init.mainloop()
################################################################################
root = Tk()
root.title("Proximity Chat")
root.iconbitmap(resource_path("_files\\icon.ico"))


def serverconn():
    global usr
    # print(Connect.get())
    host_win = Toplevel()
    host_win.title("\n")
    host_win.iconbitmap(resource_path("_files\\icon.ico"))

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

    ipinput.insert(0, "127.0.0.1")
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
    host_win.iconbitmap(resource_path("_files\\icon.ico"))

    center(host_win, 100, 0, 0, 0)
    host_win.resizable(False, False)

    # init.overrideredirect(True)

    def create_server():
        nameout = name.get()
        portout = port.get()
        ipout = ip.get()
        if ipout:
            ipout = '127.0.0.1'
        else:
            ipout = '0.0.0.0'
        os.system("start %s/Server.exe %s %s %s" % (workdir, ipout, portout, nameout.replace(' ', ';')))
        exit_win(host_win)

    def limit_input(*args):
        value = name.get()
        if len(value) > 30:
            name.set(value[:30])

    def limit_input2(*args):
        value = port.get()
        if len(value) > 5:
            port.set(value[:5])

    name = StringVar()
    name.trace('w', limit_input)
    port = StringVar()
    port.trace('w', limit_input2)
    ip = IntVar()

    namelabel = Label(host_win, text="Server Name:")
    portlabel = Label(host_win, text="Server Port:")
    iplabel = Label(host_win, text="LAN?")
    nameinput = Entry(host_win, textvariable=name, width=20)
    portinput = Entry(host_win, textvariable=port, width=20)
    # ipinput = Entry(host_win, textvariable=ip, width=20)
    ipinput = Checkbutton(host_win, variable=ip)

    nameinput.insert(0, f"{usr}'s Server")
    portinput.insert(0, "60501")
    ip.set(1)

    create_server = Button(host_win, text="Create Server", command=create_server)

    namelabel.grid(row=1, sticky=E)
    portlabel.grid(row=2, sticky=E)
    iplabel.grid(row=3, sticky=E)

    nameinput.grid(row=1, column=2, sticky=W)
    portinput.grid(row=2, column=2, sticky=W)
    ipinput.grid(row=3, column=2, sticky=W)

    create_server.grid(columnspan=3)


def options_pass():
    global usr
    host_win = Toplevel()
    host_win.title("\n")
    host_win.iconbitmap(resource_path("_files\\icon.ico"))

    center(host_win, 100, 0, 0, 0)
    host_win.resizable(False, False)

    # init.overrideredirect(True)

    def changepass():
        donevar = False
        value1 = oldpass.get()
        value2 = new1pass.get()
        value3 = new2pass.get()
        config.read(workdir + "\\profile\\localuser.dat")
        for acc in config.sections():
            if sha256(value1.encode('utf-8')).hexdigest() == config.get(acc, "Password"):
                if value2 == value3:
                    if not value2 == value1:
                        config[acc]["Password"] = sha256(value2.encode('utf-8')).hexdigest()
                        with open(workdir + "\\profile\\localuser.dat", 'w') as configfile:
                            config.write(configfile)
                        messagebox.showinfo(init, message="Password Successfully Changed")
                        donevar = True
                        exit_win(host_win)
                    else:
                        messagebox.showerror(init, message="New Password Can't Be Your Old Password")
                else:
                    messagebox.showerror(init, message="New Passwords Do Not Match")
        if donevar == False:
            messagebox.showerror(init, message="Incorrect Password")

    oldpass = StringVar()
    new1pass = StringVar()
    new2pass = StringVar()

    oldlabel = Label(host_win, text="Old Password:")
    new1label = Label(host_win, text="New Password:")
    new2label = Label(host_win, text="New Password (Again):")
    oldinput = Entry(host_win, show="•", textvariable=oldpass, width=20)
    new1input = Entry(host_win, show="•", textvariable=new1pass, width=20)
    new2input = Entry(host_win, show="•", textvariable=new2pass, width=20)

    change_pass = Button(host_win, text="Change Password", command=changepass)

    oldlabel.grid(row=1, sticky=W)
    new1label.grid(row=2, sticky=W)
    new2label.grid(row=3, sticky=W)

    oldinput.grid(row=1, column=2, sticky=E)
    new1input.grid(row=2, column=2, sticky=E)
    new2input.grid(row=3, column=2, sticky=E)

    change_pass.grid(columnspan=3)


def options_user():
    global usr
    host_win = Toplevel()
    host_win.title("\n")
    host_win.iconbitmap(resource_path("_files\\icon.ico"))

    center(host_win, 100, 0, 0, 0)
    host_win.resizable(False, False)

    # init.overrideredirect(True)

    def changeuser():
        donevar = False
        value1 = olduser.get()
        value2 = newuser.get()
        config.read(workdir + "\\profile\\localuser.dat")
        for acc in config.sections():
            if sha256(value1.encode('utf-8')).hexdigest() == config.get(acc, "Username"):
                if not value2 == value1:
                    config[acc]["Username"] = sha256(value2.encode('utf-8')).hexdigest()
                    with open(workdir + "\\profile\\localuser.dat", 'w') as configfile:
                        config.write(configfile)
                        messagebox.showinfo(init, message="Username Successfully Changed")
                    donevar = True
                    exit_win(host_win)
                else:
                    messagebox.showerror(init, message="New Username Can't Be Your Old Username")
        if donevar == False:
            messagebox.showerror(init, message="Incorrect Username")

    olduser = StringVar()
    newuser = StringVar()

    oldlabel = Label(host_win, text="Old Username:")
    newlabel = Label(host_win, text="New Username:")
    oldinput = Entry(host_win, textvariable=olduser, width=20)
    newinput = Entry(host_win, textvariable=newuser, width=20)

    change_user = Button(host_win, text="Change Username", command=changeuser)

    oldlabel.grid(row=1, sticky=W)
    newlabel.grid(row=2, sticky=W)

    oldinput.grid(row=1, column=2, sticky=E)
    newinput.grid(row=2, column=2, sticky=E)

    change_user.grid(columnspan=3)


helv = Font(family="Helvetica", size="11")
helvmen = Font(family="Helvetica", size="9")
toolbar = Frame(root)

server = Menubutton(toolbar, text="Server", font=helvmen, relief=RAISED)
server.grid()
server.menu = Menu(server, tearoff=0)
server["menu"] = server.menu

Connect = IntVar()
Host = IntVar()

server.menu.add_command(label="Connect", font=helvmen,
                        command=serverconn)
server.menu.add_command(label="Host", font=helvmen,
                        command=server_host)

server.pack(side=LEFT, padx=2, pady=2)

options = Menubutton(toolbar, text="Options", font=helvmen, relief=RAISED)
options.menu = Menu(options, tearoff=0)
options["menu"] = options.menu

option1 = IntVar()
option = IntVar()
soundvar = IntVar()
soundvar.set(1)
notifvar = IntVar()
notifvar.set(1)

options.menu.add_command(label="Change Username", font=helvmen, command=options_user)
options.menu.add_command(label="Change Password", font=helvmen, command=options_pass)
options.menu.add_checkbutton(label="Sounds", font=helvmen, variable=soundvar, onvalue=1, offvalue=0)
options.menu.add_checkbutton(label="Notifications", font=helvmen, variable=notifvar, onvalue=1, offvalue=0)

options.pack(side=RIGHT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

SList = Listbox(root, bg="WHITE", bd=3, height=30, width=15, font=helv, selectmode=SINGLE)
SList.pack(side=LEFT, fill=Y, pady=5, padx=5, anchor=W)


def onselect(evt):
    try:
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        messageSend.insert(INSERT, f'@{value} ')  # Insert blank for user input
        SList.selection_clear(0, END)
    except IndexError:
        pass


SList.bind('<<ListboxSelect>>', onselect)

Log = Text(root, bg="WHITE", bd=3, height=28, width=62, font=helv, state=DISABLED)
Log.yview_scroll(1, "units")
Log.pack(expand=1, fill=BOTH, pady=5, padx=5, anchor=W)

msgSend = StringVar()
messageSend = Entry(root, bd=3, width=103, font=helv, textvariable=msgSend)
messageSend.pack(fill=X, pady=5, padx=5, anchor=W)


# msg = messageSend.trace('w', test)


def establish_conn():
    global threadsrun, messageSend, server_address
    threadsrun = True
    Log.config(state=NORMAL)
    sock = socket(AF_INET, SOCK_STREAM)
    ip = ip_out
    port = int(port_out)
    server_address = (ip, port)
    print(server_address)
    inituser = pickle.dumps(['$inituser', usr])
    cc = pickle.dumps(['$cc', usr])
    #sock.sendto(inituser, server_address)
    Log.delete(1.0, END)

    def disband_conn():
        global threadsrun
        threadsrun = False
        root.unbind("<Return>")
        root.title("Proximity Chat")

        sock.send(cc)

        Log.config(state=NORMAL)
        Log.insert(Log.index(INSERT), "You have left the server\n")
        Log.config(state=DISABLED)
        Log.see(END)
        indx = float(Log.index(INSERT)) - 1
        Log.tag_add("leave", indx, Log.index(INSERT))
        Log.tag_config("leave", background="#FFBFBF", foreground="black", justify="center")
        SList.delete(1, END)

        server.menu.entryconfig(0, label="Connect", command=serverconn)


    server.menu.entryconfig(0, label="Disconnect", command=disband_conn)

    print("Connecting to '%s' port '%s'" % server_address)
    sock.settimeout(15)
    try:
        sock.connect(server_address)
        Log.insert(Log.index(INSERT), "Connected to '%s' port '%s'\n" % server_address)

        indx = float(Log.index(INSERT)) - 1
        Log.tag_add("conn", indx, Log.index(INSERT))
        Log.tag_config("conn", background="#A3E3ED", foreground="black", justify="center")
        sock.sendall(inituser)
    except Exception:
        print(traceback.format_exc())
        Log.insert(Log.index(INSERT), "Connection failed\n")

        indx = float(Log.index(INSERT)) - 1
        Log.tag_add("fail", indx, Log.index(INSERT))
        Log.tag_config("fail", background="#FFBFBF", foreground="black", justify="center")
        return
    finally:
        sock.settimeout(0)
        sock.setblocking(True)

    def get_message():
        global threadsrun, usr, soundvar
        try:
            while threadsrun:
                try:
                    data = sock.recv(256)
                except:
                    break
                try:
                    data = pickle.loads(data)
                    if (data[0] == '::') or (data[0] == ';;'):
                        textdata = data[1]
                except:
                    textdata = data.decode()

                if root.focus_get() is None:
                    icon = img.updateicon()
                    root.tk.call('wm', 'iconphoto', root._w, icon)
                    if notifvar.get() == 1:
                        dta = textdata.split(': ')
                        toaster.show_toast(dta[0],
                                           ': '.join(dta[1:]),
                                           icon_path=resource_path("_files\\icon.ico"),
                                           duration=5,
                                           threaded=True)
                else:
                    icon = img.geticon()
                    root.tk.call('wm', 'iconphoto', root._w, icon)

                Log.config(state=NORMAL)
                Log.insert(Log.index(INSERT), textdata + "\n")
                Log.config(state=DISABLED)
                if '@' + usr in textdata:
                    indx = float(Log.index(INSERT)) - 1
                    Log.tag_add("mention", indx, Log.index(INSERT))
                    Log.tag_config("mention", background="#FFDDAF", foreground="black", underline=1)
                if soundvar.get() == 1:
                    if '@' + usr in textdata:
                        winsound.PlaySound(resource_path("_files\\mention.wav"),
                                           winsound.SND_FILENAME | winsound.SND_ASYNC)
                    else:
                        try:
                            winsound.PlaySound(resource_path("_files\\message.wav"),
                                               winsound.SND_FILENAME | winsound.SND_ASYNC)
                        except:
                            print(traceback.format_exc())

                Log.see(END)
                if type(data) == list:
                    root.title(str(data[3]) + " - " + str(len(data[2].split('\n'))) + " online")
                    if data[0] == '::':
                        indx = float(Log.index(INSERT)) - 1
                        Log.tag_add("join", indx, Log.index(INSERT))
                        Log.tag_config("join", background="#BFFFC0", foreground="black", justify="center")
                        SList.delete(0, END)
                        for x in data[2].split('\n'):
                            SList.insert(END, x)
                    if data[0] == ';;':
                        indx = float(Log.index(INSERT)) - 1
                        Log.tag_add("leave", indx, Log.index(INSERT))
                        Log.tag_config("leave", background="#FFBFBF", foreground="black", justify="center")
                        SList.delete(0, END)
                        for x in data[2].split('\n'):
                            SList.insert(END, x)
        except:
            sock.close()
            print(traceback.format_exc())
            Log.config(state=NORMAL)
            Log.insert(Log.index(INSERT), "Connection to server lost.\n")
            Log.config(state=DISABLED)
            indx = float(Log.index(INSERT)) - 1
            Log.tag_add("lost", indx, Log.index(INSERT))
            Log.tag_config("lost", background="red", foreground="black", justify="center")

    threading.Thread(target=get_message, args=()).start()

    def send_message(var):
        try:
            global messageSend
            if not messageSend.get() == '':
                message = "%s: %s" % (usr, messageSend.get())
                message = message.replace('\n', ' ').replace('\r', ' ')
                print(message)
                messageSend.delete(0, END)
                sock.send(message.encode('utf-8'))
        except:
            print(traceback.format_exc())

    def exitroot1():
        confirm_exit = messagebox.askyesno(root, message="Are you sure you want to exit?")
        if confirm_exit:
            sock.close()
            #sock.sendto(cc, server_address)
            exit_win(root)
            sys.exit()

    root.protocol('WM_DELETE_WINDOW', exitroot1)

    root.bind("<Return>", send_message)

    Log.config(state=DISABLED)


def exitroot():
    confirm_exit = messagebox.askyesno(root, message="Are you sure you want to exit?")
    if confirm_exit:
        exit_win(root)
        sys.exit()


root.protocol('WM_DELETE_WINDOW', exitroot)

center(root, 0, 0, 0, 0)

root.mainloop()
