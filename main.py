from tkinter import *
from tkinter import ttk
from util import *
from writeFiles import *

root = Tk()
root.title("AutoNet")
root.geometry("480x200")

# #########################DEVICE FORM###################################################

def add_device():
    window = Toplevel(root)
    window.title("Add Device")
    window.geometry("400x350")
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
    frame_add.pack(pady=10)

    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def show_form(value):
        if value == 1:
            # clear frame
            clear_frame(frame_add)

            # add new widgets
            lbl_host_name = Label(frame_add, text="Name: ").grid(row=0, column=0, pady=(10,10))
            en_host_name = Entry(frame_add, width=20)
            en_host_name.grid(row=0, column=1, pady=(10,10))

            lbl_host_ip = Label(frame_add, text="IP address: ").grid(row=1, column=0)
            en_host_ip = Entry(frame_add, width=20)
            en_host_ip.grid(row=1, column=1)
            lbl_host_mask = Label(frame_add, text="Netmask: ").grid(row=2, column=0, pady=(0,10))
            en_host_mask = Entry(frame_add, width=20)
            en_host_mask.grid(row=2, column=1, pady=(0,10))

            lbl_host_gate = Label(frame_add, text="Default gateway: ").grid(row=3, column=0, pady=(0,10))
            en_host_gate = Entry(frame_add, width=20)
            en_host_gate.grid(row=3, column=1, pady=(0,10))

            serv = IntVar()
            serv.set("0")
            lbl_services = Label(frame_add, text="Services: (Optional)").grid(row=4, column=0)
            http = Radiobutton(frame_add, width=10, text="HTTP", variable=serv, value=1)
            http.grid(row=5, column=0)
            ftp = Radiobutton(frame_add, width=10, text="FTP", variable=serv, value=2)
            ftp.grid(row=5, column=1)

            btn_save = Button(frame_add, text="Save", width=25, command=lambda: new_host(en_host_name.get(),
                                                                                         en_host_ip.get(),
                                                                                         en_host_mask.get(),
                                                                                         en_host_gate.get(),
                                                                                         serv.get()))
            btn_save.grid(row=6, column=0, columnspan=2, sticky=SE, pady=30)

        elif value == 2:
            # clear frame
            clear_frame(frame_add)

            lbl_router_name = Label(frame_add, text="Name: ").grid(row=0, column=0, pady=(0,10))
            en_router_name = Entry(frame_add, width=20)
            en_router_name.grid(row=0, column=1, pady=(0,10))
            lbl_router_ip1 = Label(frame_add, text="IP address: ").grid(row=1, column=0)
            en_router_ip1 = Entry(frame_add, width=20)
            en_router_ip1.grid(row=1, column=1)
            lbl_router_mask1 = Label(frame_add, text="Netmask: ").grid(row=2, column=0, pady=(0,10))
            en_router_mask1 = Entry(frame_add, width=20)
            en_router_mask1.grid(row=2, column=1, pady=(0,10))

            # max 3 network interfaces per router

            lbl_optional2 = Label(frame_add, text="Additional interfaces").grid(row=3, column=0, columnspan=2, pady=(0,5))
            lbl_router_ip2 = Label(frame_add, text="IP address: ").grid(row=4, column=0)
            en_router_ip2 = Entry(frame_add, width=20)
            en_router_ip2.grid(row=4, column=1)
            lbl_router_mask2 = Label(frame_add, text="Netmask: ").grid(row=5, column=0, pady=(0,10))
            en_router_mask2 = Entry(frame_add, width=20)
            en_router_mask2.grid(row=5, column=1, pady=(0,10))

            lbl_router_ip3 = Label(frame_add, text="IP address: ").grid(row=6, column=0)
            en_router_ip3 = Entry(frame_add, width=20)
            en_router_ip3.grid(row=6, column=1)
            lbl_router_mask3 = Label(frame_add, text="Netmask: ").grid(row=7, column=0)
            en_router_mask3 = Entry(frame_add, width=20)
            en_router_mask3.grid(row=7, column=1)

            btn_save = Button(frame_add, text="Save", width=25, command=lambda: new_router(en_router_name.get(),
                                                                                           en_router_ip1.get(),
                                                                                           en_router_mask1.get(),
                                                                                           en_router_ip2.get(),
                                                                                           en_router_mask2.get(),
                                                                                           en_router_ip3.get(),
                                                                                           en_router_mask3.get()))
            btn_save.grid(row=8, column=0, columnspan=2, sticky=SE, pady=(10,0))

        else:
            # clear frame
            clear_frame(frame_add)

            lbl_switch_name = Label(frame_add, text="Name: ").grid(row=0, column=0, pady=(30,20))
            en_switch_name = Entry(frame_add, width=20)
            en_switch_name.grid(row=0, column=1, pady=(30,20))

            btn_save = Button(frame_add, text="Save", width=25, command=lambda: new_switch(en_switch_name.get()))
            btn_save.grid(row=1, column=0, columnspan=2, sticky=SE)

    btn_exit = Button(window, text="Exit", width=10, command=window.destroy)
    btn_exit.pack(anchor=SE, side=BOTTOM)
    window.mainloop()

# #########################LINK FORM###################################################


def add_link():
    window = Toplevel(root)
    window.title("Add Link")
    window.geometry("550x200")

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
    btn_linking.grid(row=2, column=2)

    btn_exit = Button(window, text="Exit", width=10, command=window.destroy)
    btn_exit.grid(row=3, column=2, pady=100)

    window.mainloop()


def create_net():
    write_sh()
    write_vagrant()
    launch_vagrant()

# ############################################################################


def show_topo():
    window = Toplevel(root)
    window.title("Show Topology")
    window.geometry("1000x700")

    show_tree(window)

    window.mainloop()


# ############################################################################

lbl_step1 = Label(root, width=40, text="Step-1: Add Devices to create the network", anchor="w")
lbl_step1.grid(row=0, column=0, pady=10)
btn_add = Button(root, text="Add Device", width=25, command=add_device)
btn_add.grid(row=0, column=1, columnspan=2)

lbl_step2 = Label(root, width=40, text="Step-2: Create link between devices", anchor="w")
lbl_step2.grid(row=1, column=0, pady=10)
btn_link_form = Button(root, text="Create Link", width=25, command=add_link)
btn_link_form.grid(row=1, column=1, columnspan=2)

lbl_step3 = Label(root, width=40, text="Step-3: Check the created topology",anchor="w")
lbl_step3.grid(row=2, column=0, pady=10)
btn_show_net = Button(root, text="Show topology", width=25, command=show_topo)
btn_show_net.grid(row=2, column=1, columnspan=2)

lbl_step4 = Label(root, width=40, text="Step-4: Create and Run the network", anchor="w")
lbl_step4.grid(row=3, column=0, pady=10)
btn_create = Button(root, text="Create & Run", width=25, command=create_net)
btn_create.grid(row=3, column=1, columnspan=2)

lbl_step5 = Label(root, width=40, text="Step-5: Delete configuration files", anchor="w")
lbl_step5.grid(row=4, column=0, pady=10)
btn_destroy = Button(root, text="Destroy", width=25, command=destroy_net)
btn_destroy.grid(row=4, column=1, columnspan=1)

root.mainloop()


