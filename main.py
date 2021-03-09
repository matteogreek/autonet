from tkinter import *
from dataclasses import dataclass
from tkinter import ttk
from typing import List

host_list = []
switch_list = []
router_list = []

@dataclass
class Host:
    name: str
    ip: str
    mask: str
    gateway: str

    def __str__(self):
        return self.name

'''
    link: str #dovrebbe essere una lista

    def __init__(self, name, ip, mask, gateway, link=None):
        self.name = name
        self.name = ip
        self.name = mask
        self.name = gateway
        self.link = link
        
 p = Point(1.5, 2.5)
 print(p)  # Point(x=1.5, y=2.5, z=0.0)
'''

@dataclass
class Router:
    name: str
    ip = {}
    route: str

    def __str__(self):
        return self.name


@dataclass
class Switch:
    name: str
    link: str

    def __init__(self, name, link=None):
        self.name = name
        self.link = link

    def __str__(self):
        return self.name


root = Tk()
root.title("AutoNet")
root.geometry("200x200")


def new_host(name, ip, mask, gate):
    h = Host(name, ip, mask, gate)
    for i in host_list:
        if name == i.name or ip == i.ip:
            print("esiste già")
            return 0
    host_list.append(h)

    for i in host_list:
        print(i)


def new_switch(name):
    s = Switch(name)
    for i in switch_list:
        if name == i.name:
            print("esiste già")
            return 0
    switch_list.append(s)

    for i in switch_list:
        print(i)


def new_router(name, ip, route):
    r = Router(name, ip, route)
    host_list.append(r)


def write_switch_file(sname):
    f = open(sname + ".sh", "w")
    f.write("prova")
    f.close()


def write_host_file(sname):
    f = open(sname + ".sh", "w")
    f.write("prova")
    f.close()


def write_router_file(sname):
    f = open(sname + ".sh", "w")
    f.write("prova")
    f.close()


def add_device():
    window = Toplevel(root)
    window.title("Add Device")
    window.geometry("400x400")
    top_frame = Frame(window)
    top_frame.pack()

    lbl = Label(top_frame, width=25, text="Choose a device to add")
    lbl.pack()

    v = IntVar()
    v.set("0")

    # Host=1, router=2, switch=3
    rdb1 = Radiobutton(top_frame, width=10, text="Host-PC", variable=v, value=1, command=lambda: show_form(v.get()))
    rdb2 = Radiobutton(top_frame, width=10, text="Router", variable=v, value=2, command=lambda: show_form(v.get()))
    rdb3 = Radiobutton(top_frame, width=10, text="Switch", variable=v, value=3, command=lambda: show_form(v.get()))
    rdb1.pack(anchor=NW, side=LEFT)
    rdb2.pack(anchor=NW, side=LEFT)
    rdb3.pack(anchor=NW, side=LEFT)

    frame_add = Frame(window, relief=SUNKEN)
    frame_add.pack()

    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def show_form(value):
        if value == 1:
            # clear frame
            clear_frame(frame_add)

            # add new widgets
            lbl_host_name = Label(frame_add, text="Name: ").grid(row=0, column=0)
            en_host_name = Entry(frame_add, width=20)
            en_host_name.grid(row=0, column=1)
            lbl_host_ip = Label(frame_add, text="IP address: ").grid(row=1, column=0)
            en_host_ip = Entry(frame_add, width=20)
            en_host_ip.grid(row=1, column=1)
            lbl_host_mask = Label(frame_add, text="Netmask: ").grid(row=2, column=0)
            en_host_mask = Entry(frame_add, width=20)
            en_host_mask.grid(row=2, column=1)
            lbl_host_gate = Label(frame_add, text="Default gateway: ").grid(row=3, column=0)
            en_host_gate = Entry(frame_add, width=20)
            en_host_gate.grid(row=3, column=1)

            btn_save = Button(frame_add, text="Save", width=25, command=lambda: new_host(en_host_name.get(),
                                                                                         en_host_ip.get(),
                                                                                         en_host_mask.get(),
                                                                                         en_host_gate.get()))
            btn_save.grid(row=4, column=0, columnspan=2, sticky=SE)
            print("host")
        elif value == 2:
            # clear frame
            clear_frame(frame_add)

            lbl_router_name = Label(frame_add, text="Name: ").grid(row=0, column=0)
            en_router_name = Entry(frame_add, width=20).grid(row=0, column=1)

            # max 3 network interfaces per router
            lbl_router_ip1 = Label(frame_add, text="IP address: ").grid(row=1, column=0)
            en_router_ip1 = Entry(frame_add, width=20)
            en_router_ip1.grid(row=1, column=1)
            lbl_router_mask1 = Label(frame_add, text="Netmask: ").grid(row=2, column=0)
            en_router_mask1 = Entry(frame_add, width=20)
            en_router_mask1.grid(row=2, column=1)
            lbl_router_ip2 = Label(frame_add, text="IP address: ").grid(row=3, column=0)
            en_router_ip2 = Entry(frame_add, width=20)
            en_router_ip2.grid(row=3, column=1)
            lbl_router_mask2 = Label(frame_add, text="Netmask: ").grid(row=4, column=0)
            en_router_mask2 = Entry(frame_add, width=20)
            en_router_mask2.grid(row=4, column=1)
            lbl_router_ip3 = Label(frame_add, text="IP address: ").grid(row=5, column=0)
            en_router_ip3 = Entry(frame_add, width=20)
            en_router_ip3.grid(row=5, column=1)
            lbl_router_mask3 = Label(frame_add, text="Netmask: ").grid(row=6, column=0)
            en_router_mask3 = Entry(frame_add, width=20)
            en_router_mask3.grid(row=6, column=1)

            lbl_router_route = Label(frame_add, text="IP route: ").grid(row=7, column=0)  # 1 non basta?
            en_router_route = Entry(frame_add, width=20)
            en_router_route.grid(row=7, column=1)

            btn_save = Button(frame_add, text="Save", width=25, command=write_switch_file(en_router_route.get()))
            btn_save.grid(row=8, column=0, columnspan=2, sticky=SE)
            print("router")
        else:
            # clear frame
            clear_frame(frame_add)

            lbl_switch_name = Label(frame_add, text="Name: ").grid(row=0, column=0)
            en_switch_name = Entry(frame_add, width=20)
            en_switch_name.grid(row=0, column=1)

            btn_save = Button(frame_add, text="Save", width=25, command=lambda: new_switch(en_switch_name.get()))
            btn_save.grid(row=1, column=0, columnspan=2, sticky=SE)
            print("switch")

    window.mainloop()
##########################LINK FORM###################################################


def add_combo(lista, combo):
    for i in lista:
        combo['values'] += (i.name,)

def findName(name, lista):
    for i in lista:
        if i.name == name:
           #i.link = "enp0s8"
            print("trovato")

def chosingVar(varHost, varSwitch, varRouter):
    h = varHost.get()
    s = varSwitch.get()
    r = varRouter.get()

    findName(h, host_list)
    findName(s, switch_list)
    findName(r, router_list)

    print("host " + h)
    print("switch " + r)


def add_link():
    window = Toplevel(root)
    window.title("Add Link")
    window.geometry("550x200")

    #frame_add = Frame(window, relief=SUNKEN)
    #frame_add.grid(column=0, row=0)

    for i in range(3):
        window.columnconfigure(i, weight=1)

    lbl = Label(window, width=25, text="Select 2 devices to create link")
    lbl.grid(row=0, column=0)

    lbl_host = Label(window, width=25, text="Select host")
    lbl_host.grid(row=1, column=0, padx=(5, 5))
    host = StringVar()
    combobox_host = ttk.Combobox(window, width=15, textvariable=host, value=host_list)
    combobox_host.grid(row=2, column=0, padx=(5, 5))

    lbl_switch = Label(window, width=25, text="Select switch")
    lbl_switch.grid(row=1, column=1, padx=(5, 5))
    switch = StringVar()
    combobox_switch = ttk.Combobox(window, width=15, textvariable=switch, value=switch_list)
    combobox_switch.grid(row=2, column=1, padx=(5, 5))

    lbl_router = Label(window, width=25, text="Select router")
    lbl_router.grid(row=1, column=2, padx=(5, 5))
    router = StringVar()
    combobox_router = ttk.Combobox(window, width=15, textvariable=router)
    add_combo(router_list, combobox_router)
    combobox_router.grid(row=2, column=2, padx=(5, 5))

    btn_linking = Button(window, text="Create link", width=10, command=lambda: chosingVar(host, switch, router))
    btn_linking.grid(row=3, column=2, sticky='se')

    '''
    def callbackFunc(event):
        print("New Element Selected")

    combobox_host.bind("<<ComboboxSelected>>", callbackFunc)
    '''







    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()


    window.mainloop()

btn_add = Button(root, text="Add Device", width=25, command=add_device)
btn_add.pack()
btn_link_form = Button(root, text="Create Link", width=25, command=add_link)
btn_link_form.pack()

root.mainloop()