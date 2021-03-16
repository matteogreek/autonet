from tkinter import *
from dataclasses import dataclass
from tkinter import ttk
from typing import List

host_list = []
switch_list = []
router_list = []

device_list = []

@dataclass
class Host:
    def __init__(self, name, ip, mask, gateway):
        self.name = name
        self.ip = ip
        self.mask = mask
        self.gateway = gateway
        self.link = []

    def __str__(self):
        return self.name


@dataclass
class Router:
    name: str
    ip = {}
    route: str


    #def __str__(self):
       # return self.name


@dataclass
class Switch:

    def __init__(self, name):
        self.name = name
        self.link = []


    def __str__(self):
        return self.name



root = Tk()
root.title("AutoNet")
root.geometry("200x200")


def new_host(name, ip, mask, gate):

    h = Host(name, ip, mask, gate)

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


def mask_in_slash(netmask):
    return sum(bin(int(x)).count('1') for x in netmask.split('.'))


def write_sh():
    '''
    The syntax of isinstance() is:

    isinstance(object, classinfo)
    isinstance() Parameters
    isinstance() takes two parameters:

    object - object to be checked
    classinfo - class, type, or tuple of classes and types
    '''

    for x in device_list:
        if hasattr(x,'ip'):
            f = open(x.name + ".sh", "w")
            f.write("export DEBIAN_FRONTEND=noninteractive\n"
                    "sudo apt install -y curl\n"
                    "sudo ip addr add " + x.ip + "/" + str(mask_in_slash(x.mask)) + " dev enp0s8\n"
                    "sudo ip link set enp0s8 up\n"
                    "sudo ip route add default via "+x.gateway)
            f.close()
        else:
            f = open(x.name + ".sh", "w")
            f.write("export DEBIAN_FRONTEND=noninteractive\n"
                    "apt-get update\n"
                    "apt-get install -y openvswitch-common openvswitch-switch apt-transport-https ca-certificates curl software-properties-common\n"
                    "sudo ovs-vsctl add-br switch\n")

            for l in range(8, 8+len(x.link)):
                f.write("sudo ovs-vsctl add-port switch enp0s" + str(l) + "\n")
                f.write("sudo ip link set enp0s" + str(l) + " up\n")

            f.close()


def write_vagrant():
    f = open("Vagrantfile", "w")
    f.write("#-*- mode: ruby -*-\n"
            "# vi: set ft=ruby :\n"
            "\n"
            "# All Vagrant configuration is done below. The \"2\" in Vagrant.configure\n"
            "# configures the configuration version (we support older styles for\n"
            "# backwards compatibility). Please don't change it unless you know what\n"
            "# you're doing.\n"
            "Vagrant.configure(\"2\") do |config|\n"
            "  config.vm.box_check_update = false\n"
            "  config.vm.provider \"virtualbox\" do |vb|\n"
            "    vb.customize [\"modifyvm\", :id, \"--usb\", \"on\"]\n"
            "    vb.customize [\"modifyvm\", :id, \"--usbehci\", \"off\"]\n"
            "    vb.customize [\"modifyvm\", :id, \"--nicpromisc2\", \"allow-all\"]\n"
            "    vb.customize [\"modifyvm\", :id, \"--nicpromisc3\", \"allow-all\"]\n"
            "    vb.customize [\"modifyvm\", :id, \"--nicpromisc4\", \"allow-all\"]\n"
            "    vb.customize [\"modifyvm\", :id, \"--nicpromisc5\", \"allow-all\"]\n"
            "    vb.cpus = 1\n"
            "  end\n")
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

            btn_save = Button(frame_add, text="Save", width=25)
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


def chosingVar(first, second):
    h = first.get()
    s = second.get()

    for i in device_list:
        if i.name == h or i.name == s:
            i.link.append("broadcast_"+h)
            print("ciao a tutti ")
            print("link di "+i.name+" = ")
            print(i.link)


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

    lbl_first = Label(window, width=25, text="Select first device")
    lbl_first.grid(row=1, column=0, padx=(5, 5))
    first = StringVar()
    combobox_first = ttk.Combobox(window, width=15, textvariable=first, value=device_list)
    combobox_first.grid(row=2, column=0, padx=(5, 5))

    lbl_second = Label(window, width=25, text="Select second device")
    lbl_second.grid(row=1, column=1, padx=(5, 5))
    second = StringVar()
    combobox_second = ttk.Combobox(window, width=15, textvariable=second, value=device_list)
    combobox_second.grid(row=2, column=1, padx=(5, 5))

    btn_linking = Button(window, text="Create link", width=10, command=lambda: chosingVar(first, second))
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


def create_net():

    write_sh()
    write_vagrant()




btn_add = Button(root, text="Add Device", width=25, command=add_device)
btn_add.pack()
btn_link_form = Button(root, text="Create Link", width=25, command=add_link)
btn_link_form.pack()
btn_create = Button(root, text="Create & Run", width=25, command=create_net)
btn_create.pack()

root.mainloop()