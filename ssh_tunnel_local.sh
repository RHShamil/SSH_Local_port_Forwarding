#!/bin/bash

LOGFILE="/var/log/ssh_port_forward.log"
NOW="$(date +%d/%m/%Y' - '%H:%M)" 

REMOTEHOST="ubuntu"
REMOTEHOSTIP="18.136.118.1"
REMOTELOCALIP="10.0.2.81"

SSH_REMOTEPORT=3306
SSH_LOCALPORT=3306

createTunnel() {
    /usr/bin/ssh -f -N -i /root/code/aws-pulumi-infra/key-pair-poridhi-poc.pem -L $SSH_LOCALPORT:$REMOTELOCALIP:$SSH_REMOTEPORT $REMOTEHOST@$REMOTEHOSTIP
    
    if [[ $? -eq 0 ]]; then
        echo "[$NOW] Tunnel to $REMOTEHOST created successfully" >> $LOGFILE
    else
        echo "[$NOW] An error occurred creating a tunnel to $REMOTEHOST. RC was $?" >> $LOGFILE
    fi
}

createTunnel

