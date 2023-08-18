#!/bin/bash

# Check if the current user is root or has sudo privileges
if [[ $(id -u) -ne 0 ]]; then
  echo "This script must be run as root or with sudo privileges."
  exit 1
fi

check_kubelet() {
  if pgrep -x "kubelet" &>/dev/null ; then
    return 0  # kubelet is installed and running
  else
    return 1 
  fi
}

check_node_exporter_running() {
  if pgrep -x "node_exporter" &>/dev/null ; then
    return 0  # node_exporter is running
  else
    return 1
  fi
}

install_node_exporter() {
  /usr/bin/systemctl start node_exporter
}

# Main script logic
if [[ $(check_kubelet;echo $?) -eq 0 ]]; then
  echo "kubelet is installed and running. Skipping node_exporter installation."
  exit 0
fi

if [[ $(check_node_exporter_running;echo $?) -eq 0 ]]; then
  echo "node_exporter is installed and running. Skipping node_exporter installation."
  exit 0
fi

install_node_exporter

