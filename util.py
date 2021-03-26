from dataclasses import dataclass
import os

device_list = []


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
    # da sistemare, se seleziono come primo dispositivo uno switch o un router
    # si creano più collegamenti con lo stesso nome. Errore
    h = first.get()
    s = second.get()

    for i in device_list:
        if i.name == h or i.name == s:
            i.link.append("broadcast_"+h)
            print("ciao a tutti ")
            print("link di "+i.name+" = ")
            print(i.link)


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
