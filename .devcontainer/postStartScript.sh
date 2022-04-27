#!/bin/bash

#pulp server is on a subnet that conflicts with the default docker range,
#so we set a specific route for the pulp server

#get ip of pulp server
ip=$(dig $PULP_SERVER +short)

#get gateway
gw=$(route -n | grep 'UG[ \t]' | awk '{print $2}')

#idempotentally set the route
sudo ip route del $ip/32 via $gw dev eth0 2>/dev/null
sudo ip route add $ip/32 via $gw dev eth0

#vscode resets .bashrc to their default at container start,
#and then we append the following to switch to starship
#starship is installed via Dockerfile
echo 'eval "$(starship init bash)"' >> ~/.bashrc

#copy starship config
mkdir -p ~/.config && cp ./.devcontainer/starship.toml ~/.config/starship.toml
