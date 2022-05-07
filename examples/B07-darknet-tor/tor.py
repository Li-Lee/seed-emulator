#!/usr/bin/env python3

import sys
import json
import socket
import time
from stem import CircStatus, CircPurpose
from stem.control import Controller, EventType

TARGET_ADDR = "127.0.0.1"
PORT_NUM = 9051
PASSWORD = "password"
  
host_ip = socket.gethostbyname(socket.gethostname())
controller = Controller.from_port(address=TARGET_ADDR, port = PORT_NUM)
controller.authenticate(password=PASSWORD)

def main():

  if sys.argv[1] == "list_tor_circuits":
    listTorCircuits()

  if sys.argv[1] == "update_tor_circuit":
    updateTorCircuit(sys.argv[2], sys.argv[3], sys.argv[4])

  controller.close()


def listTorCircuits():
  circuits = []

  for circ in sorted(controller.get_circuits()):
    if circ.status != CircStatus.BUILT:
      continue
      
    prev = host_ip
    paths = []
    for circ_index, entry in enumerate(circ.path):
      div = '+' if (circ_index == len(circ.path) - 1) else '|'
      fingerprint, nickname = entry

      desc = controller.get_network_status(fingerprint, None)
      if desc:
        address = desc.address
      else:
        continue

      paths.append({"from": prev, "to": address})

      prev = address

    if len(paths) == 0:
      continue
      
    circuits.append({"id": circ.id, "purpose":circ.purpose, "paths": paths})

  print(json.dumps(circuits))  

def updateTorCircuit(circuit_id, action, parameter):
  if action == "close":
    controller.close_circuit(circuit_id)
    print("finish")

if __name__ == "__main__":
  main()


