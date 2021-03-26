from util import *


def write_sh():
    for x in device_list:
        if isinstance(x, Host):
            f = open(x.name + ".sh", "w")
            f.write("export DEBIAN_FRONTEND=noninteractive\n"
                    "sudo apt install -y curl\n"
                    "sudo ip addr add " + x.ip + "/" + str(mask_in_slash(x.mask)) + " dev enp0s8\n"
                    "sudo ip link set enp0s8 up\n"
                    "sudo ip route add default via "+x.gateway+"\n")

            #aggiunta di servizi se scelti nella form
            if x.service != 0:
                f.write("sudo apt-get update\n"
                        "sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common\n"
                        "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -\n"
                        "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"\n"
                        "sudo apt-get update\n"
                        "sudo apt-get install -y docker-ce docker-ce-cli containerd.io\n")

                if x.service == 1:  # HTTP
                    f.write("sudo docker pull dustnic82/nginx-test\n"
                            "sudo docker run -d -p 80:80 dustnic82/nginx-test\n")

                if x.service == 2:  # FTP
                    f.write("docker pull panubo/vsftpd\n"
                            "docker run --rm -it -p 21:21 -p 4559-4564:4559-4564 -e FTP_USER=ftp -e FTP_PASSWORD=ftp\n")

            f.close()

        if isinstance(x, Switch):
            f = open(x.name + ".sh", "w")
            f.write("export DEBIAN_FRONTEND=noninteractive\n"
                    "apt-get update\n"
                    "apt-get install -y openvswitch-common openvswitch-switch apt-transport-https ca-certificates curl software-properties-common\n"
                    "sudo ovs-vsctl add-br switch\n")

            for l in range(8, 8+len(x.link)):
                f.write("sudo ovs-vsctl add-port switch enp0s" + str(l) + "\n")
                f.write("sudo ip link set enp0s" + str(l) + " up\n")
            f.close()

        if isinstance(x, Router):
            f = open(x.name + ".sh", "w")
            f.write("export DEBIAN_FRONTEND=noninteractive\n"
                    "sudo apt install -y curl\n")

            c = 8
            for i in x.interface.items():     # genera tuple: x[0] == IP x[1] == MASK
                if i[0] != '':
                    f.write("sudo ip addr add " + i[0] + "/" + str(mask_in_slash(i[1])) + " dev enp0s"+str(c)+"\n"
                            "sudo ip link set enp0s"+str(c)+" up\n")
                    c += 1
            f.write("sudo sysctl net.ipv4.ip_forward=1\n")
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

    for x in device_list:
        f.write("   config.vm.define \"" + x.name + "\" do |" + x.name + "|\n"
                "       " + x.name + ".vm.box = \"ubuntu/bionic64\"\n"
                "       " + x.name + ".vm.hostname = \"" + x.name + "\"\n")
        for l in x.link:
            f.write("       " + x.name + ".vm.network \"private_network\", virtualbox__intnet: \"" + l + "\", auto_config: false\n")

        f.write("       " + x.name + ".vm.provision \"shell\", path: \"" + x.name + ".sh" + "\", run: 'always'\n")
        f.write("       " + x.name + ".vm.provider \"virtualbox\" do |vb|\n"
                "           vb.memory = 256\n"
                "       end\n"
                "   end\n")
    f.write("end")
    f.close()

