#!/bin/bash

#vscode resets .bashrc to their default at container start,
#and then we append the following to switch to starship
#starship is installed via Dockerfile
echo 'eval "$(starship init bash)"' >> ~/.bashrc

#copy starship config
mkdir -p ~/.config && cp ./.devcontainer/starship.toml ~/.config/starship.toml
