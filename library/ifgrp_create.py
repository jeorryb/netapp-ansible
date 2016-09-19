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
module: ifgrp_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create ifgrp
description:
  - Ansible module to create ifgrp's on NetApp CDOT arrays via the NetApp python SDK.
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
  node:
    required: True
    description:
      - "Name of the ifgrp's node"
  ifgrp:
    required: True
    description:
      - "Name of the ifgrp; e.g. a0a|a0b"
  mode:
    required: True
    description:
      - "link policy for the ifgrp"
  dist_func:
    required: True
    description:
      - "Specifies the traffic distribution function for the ifgrp"


'''

EXAMPLES = '''
# Create ifgrp
- name: Create ifgrp a0a
    ifgrp_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      node: "atlcdot-01"
      ifgrp: "a0a"
      mode: "multimode_lacp"
      dist_func: "ip"

'''

def ifgrp_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  node = module.params['node']
  ifgrp = module.params['ifgrp']
  mode = module.params['mode']
  dist_func = module.params['dist_func']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("net-port-ifgrp-create")
  api.child_add_string("distribution-function", dist_func)
  api.child_add_string("ifgrp-name", ifgrp)
  api.child_add_string("mode", mode)
  api.child_add_string("node", node)


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
      node=dict(required=True),
      dist_func=dict(default='ip', choices=['mac', 'ip', 'sequential', 'port']),
      ifgrp=dict(required=True),
      mode=dict(default='multimode_lacp', choices=['multimode_lacp', 'multimode', 'singlemode']),

    ),
    supports_check_mode = False
  )

  results = ifgrp_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




