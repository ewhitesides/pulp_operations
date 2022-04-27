#!/bin/bash

#install dependencies from setup.py, rm the stuff that is built
pip3 install --user -r requirements.txt

#make logging folder and chown to vscode user
sudo mkdir -p /var/log/pulp_operations && sudo chown vscode:vscode /var/log/pulp_operations
