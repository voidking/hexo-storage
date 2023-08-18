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

# Function to check if Docker is installed and running
check_docker() {
  if command -v docker &>/dev/null && docker info &>/dev/null; then
    return 0  # Docker is installed and running
  else
    return 1  # Docker is not installed or not running
  fi
}

# Function to check if cAdvisor container is exist
check_cadvisor() {
  if docker ps -a --format '{{.Names}}' | grep -q "cadvisor"; then
    return 0  # cAdvisor container is exist
  else
    return 1  # cAdvisor container is not exist
  fi
}

# Function to check if cAdvisor container is running
check_cadvisor_running() {
  if docker ps --format '{{.Names}}' | grep -q "cadvisor"; then
    return 0  # cAdvisor container is running
  else
    return 1  # cAdvisor container is not running
  fi
}

# Function to start cAdvisor container
start_cadvisor() {
  docker start cadvisor
}

# Function to install cAdvisor
install_cadvisor() {
  # Install prerequisites (e.g., curl) if needed
  # For example, on Debian/Ubuntu:
  # apt-get update
  # apt-get install -y curl

  # Install cAdvisor using the provided installation method
  # For example, for cAdvisor on Docker:
  docker run -d --name=cadvisor \
  --privileged \
  --device=/dev/kmsg \
  -p 9101:8080 \
  -v /:/rootfs:ro \
  -v /var/run:/var/run:ro \
  -v /sys:/sys:ro \
  -v /var/lib/docker/:/var/lib/docker:ro \
  -v /dev/disk/:/dev/disk:ro \
  gcr.dockerproxy.com/cadvisor/cadvisor:v0.47.1 \
  --housekeeping_interval=30s \
  --max_housekeeping_interval=35s \
  --global_housekeeping_interval=30s \
  --allow_dynamic_housekeeping=true \
  --event_storage_event_limit=default=0 \
  --event_storage_age_limit=default=0 \
  --storage_duration=1m0s \
  --store_container_labels=false \
  --whitelisted_container_labels=io.kubernetes.container.name,io.kubernetes.pod.name,io.kubernetes.pod.namespace \
  --docker_only=true \
  --disable_metrics=advtcp,cpu_topology,cpuset,hugetlb,memory_numa,process,referenced_memory,resctrl,sched,tcp,udp,percpu,perf_event,disk,diskIO
}

# Main script logic
if [[ $(check_kubelet;echo $?) -eq 0 ]]; then
  echo "kubelet is installed and running. Skipping cAdvisor installation."
  exit 0
fi

if [[ $(check_docker;echo $?) -ne 0 ]]; then
  echo "Docker is not installed or not running. Skipping cAdvisor installation."
  exit 0
fi

if [[ $(check_cadvisor;echo $?) -eq 0 ]];then
  if [[ $(check_cadvisor_running; echo $?) -ne 0 ]];then
    echo "cAdvisor is not running. Start it ..."
    start_cadvisor
  else
    echo "cAdvisor is running."
  fi
else
  echo "cAdvisor is not installed. Install it ..."
  install_cadvisor
fi 
