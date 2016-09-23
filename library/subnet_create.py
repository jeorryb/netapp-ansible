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

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  subnet_name = module.params['subnet_name']
  subnet = module.params['subnet']
  ip_ranges = module.params['ip_ranges']
  bc_domain = module.params['bc_domain']
  gateway = module.params['gateway']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

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
      subnet_name=dict(required=True),
      subnet=dict(required=True),
      ip_ranges=dict(required=True, type='list'),
      bc_domain=dict(required=True),
      gateway=dict(required=False),

    ),
    supports_check_mode = False
  )

  results = subnet_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




