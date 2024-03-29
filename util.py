from dataclasses import dataclass
import os
from tkinter import *
from tkinter import ttk

device_list = []
c = 0


@dataclass
class Host:
    def __init__(self, name, ip, mask, gateway, service):
        self.name = name
        self.ip = ip
        self.mask = mask
        self.gateway = gateway
        self.link = []
        self.service = service

    def __str__(self):
        return self.name


@dataclass
class Router:
    def __init__(self, name):
        self.name = name
        self.interface = {}
        self.link = []

    def __str__(self):
        return self.name


@dataclass
class Switch:
    def __init__(self, name):
        self.name = name
        self.link = []

    def __str__(self):
        return self.name


def new_host(name, ip, mask, gate, serv):

    h = Host(name, ip, mask, gate, serv)
    print(h.name + " " + h.ip + " " + h.mask + " " + h.gateway + " " + str(h.service))
    trovato = False
    for i in device_list:
        if isinstance(i, Host):
            if name == i.name or ip == i.ip:
                print("esiste già")
                trovato = True
    if not trovato:
        device_list.append(h)



def new_switch(name):
    s = Switch(name)

    trovato = False
    for i in device_list:
        if name == i.name:
            print("esiste già")
            trovato = True
    if not trovato:
        device_list.append(s)


def new_router(name, ip1, m1, ip2, m2, ip3, m3):

    r = Router(name)
    r.interface = {ip1: m1, ip2: m2, ip3: m3}

    trovato = False
    for i in device_list:
        if name == i.name:
            print("esiste già")
            trovato = True
    if not trovato:
        device_list.append(r)


def mask_in_slash(netmask):
    return sum(bin(int(x)).count('1') for x in netmask.split('.'))


def chosingVar(first, second):
    f = first.get()
    s = second.get()
    for i in device_list:
        if i.name == f or i.name == s:
            i.link.append("broadcast_" + f + "_" + s)


def destroy_net():
    if os.name == 'nt':     # Windows
        delete_sh = os.system("del \"*.sh\" /s /f /q")
        print("delete ran with exit code %d" % delete_sh)
    else:                   # Linux
        delete_sh = os.system("find . -type f -iname *.sh -delete")
        print("delete ran with exit code %d" % delete_sh)


def launch_vagrant():
    launch = os.system("vagrant up")
    print("vagrant up ran with exit code %d" % launch)

    if launch == 0:
        print("Checking status of machines:\n")
        status = os.system("vagrant status")
        print("vagrant status ran with exit code %d" % status)


def show_tree(window):

    label_h = Label(window, width=20, text="Host list").pack()
    cols = ('name', 'ip', 'mask', 'gateway', 'link')
    treehost = ttk.Treeview(window, columns=cols, show='headings')
    treehost.pack(expand=True, fill="both")
    for col in cols:
        treehost.heading(col, text=col)

    label_r = Label(window, width=20, text="Router list").pack()
    cols2 = ('name', 'interface', 'link')
    treerouter = ttk.Treeview(window, columns=cols2, show='headings')
    treerouter.pack(expand=True, fill="both")
    for col in cols2:
        treerouter.heading(col, text=col)

    label_s = Label(window, width=20, text="Switch list").pack()
    cols3 = ('name', 'link')
    treeswitch = ttk.Treeview(window, columns=cols3, show='headings')
    treeswitch.pack(expand=True, fill="both")
    for col in cols3:
        treeswitch.heading(col, text=col)

    for x in device_list:
        if isinstance(x, Host):
            treehost.insert("", "end", values=(x.name,x.ip,x.mask,x.gateway,x.link))
        if isinstance(x, Router):
            treerouter.insert("", "end", values=(x.name,x.interface,x.link))
        if isinstance(x, Switch):
            treeswitch.insert("", "end", values=(x.name,x.link))