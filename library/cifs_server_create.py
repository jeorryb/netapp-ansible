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
module: cifs_server_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create CIFS Server
description:
  - Ansible module to create CIFS server on NetApp CDOT arrays via the NetApp python SDK.

requirements: ['NetApp Manageability SDK']

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
  vserver:
    required: True
    description:
      - "name of the vserver"
  cifs_user:
    required: True
    description:
      - "Username of account used to add cifs server to active directory."
  cifs_pass:
    required: True
    description:
      - "Password of account used to add cifs server to active directory."
  admin_status:
    required: False
    description:
      - "CIFS Server administrative status possible values."
    choices: ['down', 'up']
  cifs_server:
    required: True
    description:
      - "NETBIOS name of the CIFS server."
  comment:
    required: False
    description:
      - "CIFS server description."
  domain:
    required: True
    description:
      - ""
'''

EXAMPLES = '''
# Resize Volume
- name: Resize volume
    vol_size:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      volume: "documents"
      size: "2tb"

'''

def vol_size(module):

    volume = module.params['volume']
    size = module.params['size']

    results = {}
    results['changed'] = False

    api = NaElement("volume-size")
    api.child_add_string("volume",volume)
    api.child_add_string("new-size",size)
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
        volume=dict(required=True),
        size=dict(required=True),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    results = vol_size(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




