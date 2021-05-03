# Autonet
This is an academic project for the second part of the Design of Networks and Communication Systems course at the University of Trento, taught by Prof. Fabrizio Granelli.

## What is Autonet
Autonet is a Visual interface to pre-configure and run a network of VMs/containers and OpenVSwitches with the aim of automating the deployment of network setups.
The GUI of the App is done using **Tkinter** which is Python de-facto standard GUI package.
##Our Goal
Our goal is to create an application that allows the user to preconfigure and run a network of VMs.
To achieve this we have developed an application that relies on Vagrant to create, configure and run the virtual machines.

## 5 Steps
1. Device Configuration
2. Device Linking 
3. Show structure of the created network
4. Bash Scripts and VagrantFile creation for running Vagrant
5. File deletion to clean the default directory

## Implementation
* Classes are used to store the configuration of each device. 
```
@dataclass
class Host:
    def __init__(self, name, ip, mask, gateway, service):
        self.name = name
        self.ip = ip
        self.mask = mask
        self.gateway = gateway
        self.link = []
        self.service = service
```

* When the user writes the configuration of the selected device, an instance of  the class Host is created. The device is then added into device list
```
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
```
* After the creation and the linking process of the devices, there is the possibility to view the structure created.

Name  | Ip  | Mask  | Gateway  | Link
------------- | ------------- | ------------- | ------------- | -------------
Host1  | 192.168.1.2  | 255.255.255.0  | 192.168.1.1   | broadcast_Host1_Switch1

## Bash Scripts
* In order to set the configurations wrote by the user on the VM/s we use the *provision* function of Vagrant. For each device a bash script is created:
```
def write_sh():
    for x in device_list:
        if isinstance(x, Host):
            f = open(x.name + ".sh", "w")
            f.write("export DEBIAN_FRONTEND=noninteractive\n"
                    "sudo apt install -y curl\n"
                    "sudo ip addr add " + x.ip + "/" + str(mask_in_slash(x.mask)) + " dev enp0s8\n"
                    "sudo ip link set enp0s8 up\n"
                    "sudo ip route add default via "+x.gateway+"\n")
```
## VagrantFile
The primary function of the Vagrantfile is to describe the type of machine required for a project, and how to configure and provision these machines.
```
  config.vm.define "host1" do |host1|
    host1.vm.box = "ubuntu/bionic64"
    host1.vm.hostname = "host1"
    host1.vm.network "private_network", virtualbox__intnet: "broadcast_from_to", auto_config: false	
    host1.vm.provision "shell", path: "host1.sh", run: 'always'
    host1.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end
  end
```
## Create&Run
* When the *Create&Run* button is pressed: 
	1. All the bash scripts and the VagrantFile are created 
	2. **Vagrant up** and **Vagrant status** are executed

* When the command **Vagrant up** ends the network is up and running!

Made with :coffee: & :heart: by Matteo Greco, Emanuele Boscari, Thomas Dalla Via.
