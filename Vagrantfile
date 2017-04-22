# -*- mode: ruby -*-
# vi: set ft=ruby :

TR_CONFIG = {
  WORKSPACE_NAME: "twitch_recorder".freeze,
  INSTALL_DIR: "/opt/twitch_recorder".freeze
}

Vagrant.configure(2) do |config|

  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "bento/centos-7.2"
  # config.vbguest.auto_update = true

  config.vm.provider "virtualbox" do |box|
    box.name = "twitch-recorder"
  #   box.memory = 2048
  #   box.cpus = 2
  end

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  config.vm.synced_folder ".", TR_CONFIG[:INSTALL_DIR], type: "virtualbox"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.

  config.vm.provision "prepare-workspace", type: "shell", run: "always", inline: <<-SHELL
    #!/usr/bin/env bash
    [ ! -d "/vagrant/#{TR_CONFIG[:WORKSPACE_NAME]}" ] && mkdir -p "/vagrant/#{TR_CONFIG[:WORKSPACE_NAME]}"
    touch "/vagrant/#{TR_CONFIG[:WORKSPACE_NAME]}/twitch_usernames.txt"
    chmod -R 777 "/vagrant/#{TR_CONFIG[:WORKSPACE_NAME]}"
  SHELL

  config.vm.provision "setup", type: "shell", inline: <<-SHELL
    #!/usr/bin/env bash
    if [ ! -f .runonce.setup ]; then
      echo 'Initially provisioning box...'
      echo 'Updating system:'
      yum update
      yum -y install epel-release
      yum -y install python34
      curl -s -S -O https://bootstrap.pypa.io/get-pip.py
      echo 'Installing software:'
      /usr/bin/python3.4 get-pip.py && rm get-pip.py
      pip install livestreamer
      yes | rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
      yes | rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
      yum -y install ffmpeg

      touch .runonce.setup
      echo 'done'
    else
      echo 'Box has already been setup. Skipping process.'
    fi
  SHELL

  config.vm.provision "install", type: "shell", inline: <<-SHELL
    #!/usr/bin/env bash
    if [ ! -f .runonce.install ]; then
      echo 'Installing twitch recorder...'
      # Not using /vagrant/install.sh here, to enable sync for development

      # Creating symlinks for users, so that synced files will be used in any case
      ln -s "/vagrant/#{TR_CONFIG[:WORKSPACE_NAME]}" "/root"
      ln -s "/vagrant/#{TR_CONFIG[:WORKSPACE_NAME]}" "/home/vagrant"

      ln -s #{TR_CONFIG[:INSTALL_DIR]}/bin/* "/usr/bin"

      touch .runonce.install
      echo 'done'
    else
      echo 'Twitch recorder has already been installed. Skipping process.'
    fi
  SHELL

  if ARGV.include? "--provision-with"
    config.vm.provision "record", type: "shell", inline: <<-SHELL
      #!/usr/bin/env bash
      usernames_file="${HOME}/#{TR_CONFIG[:WORKSPACE_NAME]}/twitch_usernames.txt"
      if [ -s "${usernames_file}" ]; then
        echo 'Recording in the background...'
        nohup /usr/bin/record_twitch
      else
        echo "Please make sure you completed the configuration; make sure, you added usernames to '${usernames_file}'" >&2
        exit 1
      fi
    SHELL

    config.vm.provision "split", type: "shell", inline: <<-SHELL
      #!/usr/bin/env bash
      echo 'Splitting videos in the background...'
      nohup /usr/bin/split_twitch_videos
    SHELL
  end
end
