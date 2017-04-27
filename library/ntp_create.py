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
module: ntp_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create ntp server
description:
  - Ansible module to create ntp server for  NetApp CDOT via the NetApp python SDK.
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
  ntp_server:
    required: True
    description:
      - "Name or IP of the time server you wish to use"
  
'''

EXAMPLES = '''
# Create ntp server
- name: Create ntp server
    ntp_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      ntp_server: "tick.gatech.edu"

'''

def ntp_create(module):

    ntp_server = module.params['ntp_server']

    results = {}
    results['changed'] = False

    api = NaElement("ntp-server-create")
    api.child_add_string("server-name", ntp_server)

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
        ntp_server=dict(required=True),))

    results = ntp_create(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




