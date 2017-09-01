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
module: subnet_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create subnet
description:
  - Ansible module to create subnet on NetApp CDOT arrays via the NetApp python SDK.
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
  subnet_name:
    required: True
    description:
      - "Name of the subnet"
  subnet:
    required: True
    description:
      - "Specific subnet; format is <x.x.x.x/x>""
  ip_ranges:
    required: True
    description:
      - "IP address ranges containing a start an ending address; format <a.a.a.a-x.x.x.x>"
  bc_domain:
    required: True
    description:
      - "Layer 2 broadcast domain that the subnet belongs to"
  gateway:
    required: False
    description:
      - "Gateway for the default route of the subnet"


'''

EXAMPLES = '''
# Create subnet
- name: Create subnet
    subnet_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      subnet_name: "nfs"
      subnet: "10.1.10.0/24"
      ip_ranges: "10.1.10.50-10.1.10.60"
      bc_domain: "nfs"

'''

def subnet_create(module):

    subnet_name = module.params['subnet_name']
    subnet = module.params['subnet']
    ip_ranges = module.params['ip_ranges']
    bc_domain = module.params['bc_domain']
    gateway = module.params['gateway']

    results = {}
    results['changed'] = False

    api = NaElement("net-subnet-create")
    api.child_add_string("broadcast-domain", bc_domain)
    api.child_add_string("subnet-name", subnet_name)
    api.child_add_string("subnet", subnet)

    if module.params['gateway']:
        api.child_add_string("gateway", gateway)

    xi = NaElement("ip-ranges")
    api.child_add(xi)
    for ip in ip_ranges:
        xi.child_add_string("ip-range", ip)

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
        subnet_name=dict(required=True),
        subnet=dict(required=True),
        ip_ranges=dict(required=True, type='list'),
        bc_domain=dict(required=True),
        gateway=dict(required=False),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = subnet_create(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




