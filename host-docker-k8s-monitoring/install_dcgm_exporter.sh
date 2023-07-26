#!/bin/bash

# Check if the current user is root or has sudo privileges
if [[ $(id -u) -ne 0 ]]; then
  echo "This script must be run as root or with sudo privileges."
  exit 1
fi

check_docker() {
  if command -v docker &>/dev/null && docker info &>/dev/null; then
    return 0  # Docker is installed and running
  else
    return 1  # Docker is not installed or not running
  fi
}

check_nvidia() {
  if command -v nvidia-smi &>/dev/null; then
    return 0  # nvidia-smi is installed
  else
    return 1  # nvidia-smi is not installed
  fi
}

check_dcgm_exporter() {
  if docker ps -a --format '{{.Names}}' | grep -q "dcgm-exporter"; then
    return 0  # cAdvisor container is exist
  else
    return 1  # cAdvisor container is not exist
  fi
}

# Function to check if cAdvisor container is running
check_dcgm_exporter_running() {
  if docker ps --format '{{.Names}}' | grep -q "dcgm-exporter"; then
    return 0  # cAdvisor container is running
  else
    return 1  # cAdvisor container is not running
  fi
}

start_dcgm_exporter() {
  docker start dcgm-exporter
}

install_dcgm_exporter() {
  docker run -d --name=dcgm-exporter \
  --gpus all \
  --hostname=$(hostname) \
  --restart=always \
  -p 9400:9400  \
  nvcr.io/nvidia/k8s/dcgm-exporter:2.4.6-2.6.10-ubuntu20.04
}

# Main script logic
if [[ $(check_docker;echo $?) -ne 0 ]]; then
  echo "Docker is not installed or not running. Skipping dcgm-exporter installation."
  exit 0
fi

if [[ $(check_nvidia;echo $?) -ne 0 ]]; then
  echo "Nvidia is not installed. Skipping dcgm-exporter installation."
  exit 0
fi

if [[ $(check_dcgm_exporter;echo $?) -eq 0 ]];then
  if [[ $(check_dcgm_exporter_running; echo $?) -ne 0 ]];then
    echo "dcgm-exporter is not running. Start it ..."
    start_dcgm_exporter
  else
    echo "dcgm-exporter is running."
  fi
else
  echo "dcgm-exporter is not installed. Install it ..."
  install_dcgm_exporter
fi

