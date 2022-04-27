#!/bin/bash

#make logging folder and chown to vscode user
PULP_LOGDIR=$(dirname $PULP_LOGPATH)
sudo mkdir -p $PULP_LOGDIR && sudo chown vscode:vscode $PULP_LOGDIR
