#!/usr/bin/python

import sys
import json

try:
  from NaServer import *
  NASERVER_AVAILABLE = True
except ImportError:
  NASERVER_AVAILABLE = False

if not NASERVER_AVAILABLE:
    module.fail_json(msg="The NetApp Manageability SDK library is not installed")

DOCUMENTATTION = '''
---
module: cluster_peer_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create cluster peering
description:
  - Ansible module to create cluster peering relationships on NetApp CDOT arrays via the NetApp python SDK.
requirements:
  - NetApp Manageability SDK
options:
  cluster:
    required: True
    description:
      - "The ip address or hostname of the cluster"
  user_name:
    required: True
    description:
      - "Administrator user for the cluster/node"
  password:
    required: True
    description:
      - "password for the admin user"
  remote_user:
    required: False
    description:
      - "Remote cluster username"
  remote_pass:
    required: False
    description:
      - "Remote cluster password"
  peer_addrs:
    required: True
    description:
      - "Remote intercluster addresses or hostnames"


'''

EXAMPLES = '''
# Create cluster peer
- name: Cluster peer with dencdot
    cluster_peer_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      remote_user: "admin"
      remote_pass: "Password2"
      peer_addrs: ["192.168.1.170", "192.168.1.171"]

'''

def cluster_peer_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  remote_user = module.params['remote_user']
  remote_pass = module.params['remote_pass']
  peer_addrs = module.params['peer_addrs']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("cluster-peer-create")
  if module.params['remote_user']:
    api.child_add_string("user-name", remote_user)
    api.child_add_string("password", remote_pass)

  xi = NaElement("peer-addresses")
  api.child_add(xi)

  for ip in peer_addrs:
    xi.child_add_string("remote-inet-address", ip)


  xo = s.invoke_elem(api)

  if(xo.results_errno() != 0):
    r = xo.results_reason()
    module.fail_json(msg=r)
    results['changed'] = False

  else:
    results['changed'] = True

  return results

def main():
  module = AnsibleModule(
    argument_spec = dict(
      cluster=dict(required=True),
      user_name=dict(required=True),
      password=dict(required=True),
      remote_user=dict(required=False),
      remote_pass=dict(required=False),
      peer_addrs=dict(required=True, type='list'),

    ),
    supports_check_mode = False
  )

  results = ifgrp_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




