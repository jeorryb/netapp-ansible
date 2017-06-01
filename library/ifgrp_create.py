#!/usr/bin/python

import sys
import json
from  ansible.module_utils import ntap_util

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

    node = module.params['node']
    ifgrp = module.params['ifgrp']
    mode = module.params['mode']
    dist_func = module.params['dist_func']

    results = {}
    results['changed'] = False

    api = NaElement("net-port-ifgrp-create")
    api.child_add_string("distribution-function", dist_func)
    api.child_add_string("ifgrp-name", ifgrp)
    api.child_add_string("mode", mode)
    api.child_add_string("node", node)


    connection = ntap_util.connect_to_api(module)
    xo = connection.invoke_elem(api)

    if(xo.results_errno() != 0):
        r = xo.results_reason()
        module.fail_json(msg=r)
        results['changed'] = False

    else:
        results['changed'] = True

    return results

def main():

    argument_spec = ntap_util.ntap_argument_spec()
    argument_spec.update(dict(
        node=dict(required=True),
        dist_func=dict(default='ip', choices=['mac', 'ip', 'sequential', 'port']),
        ifgrp=dict(required=True),
        mode=dict(default='multimode_lacp',
                  choices=['multimode_lacp', 'multimode', 'singlemode']),))

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    results = ifgrp_create(module)



    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




