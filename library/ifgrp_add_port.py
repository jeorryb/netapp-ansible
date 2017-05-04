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
module: ifgrp_add_port
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Add port to ifgrp
description:
  - Ansible module to add ports to an  ifgrp on NetApp CDOT arrays via the NetApp python SDK.
requirements:
  - NetApp Manageability SDK
options:
  cluster:
    required: True
    description:
      - "The ip address or hostname of the cluster."
  user_name:
    required: True
    description:
      - "Administrator user for the cluster/node."
  password:
    required: True
    description:
      - "Password for the admin user."
  node:
    required: True
    description:
      - "Name of the ifgrp's node."
  ifgrp:
    required: True
    description:
      - "Name of the ifgrp; e.g. a0a|a0b."
  port:
    required: True
    description:
      - "Port being added to the ifgrp."


'''

EXAMPLES = '''
# Create ifgrp
- name: Add e0a to ifgrp a0a
    ifgrp_add_port:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      node: "atlcdot-01"
      ifgrp: "a0a"
      port: "e0a"

'''

def ifgrp_add_port(module):

    node = module.params['node']
    ifgrp = module.params['ifgrp']
    port = module.params['port']

    results = {}
    results['changed'] = False

    api = NaElement("net-port-ifgrp-add-port")
    api.child_add_string("ifgrp-name", ifgrp)
    api.child_add_string("node", node)
    api.child_add_string("port", port)

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
        ifgrp=dict(required=True),
        port=dict(required=True),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = ifgrp_add_port(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()
