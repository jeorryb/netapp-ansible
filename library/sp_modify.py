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
module: sp_modify
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Modify Service-Processor NetApp CDOT
description:
  - Ansible module to modify the NetApp CDOT Service-Processor's via the NetApp python SDK.
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
      - "Name of the Service-Processor's node"
  addr_family:
    required: False
    description:
      - "IPv4 or IPv6"
  dhcp:
    required: False
    description:
      - "dhcp status, v4 or none"
  ip:
    required: False
    description:
      - "IP address"
  netmask:
    required: False
    description:
      - "subnet mask"
  gateway:
    required: False
    description:
      - "default gateway"
  enabled:
    required: True
    description:
      - "Is the sp enabled, boolean"
'''

EXAMPLES = '''
# Modify Service Processor
- name: Modify Service Processor Settings
    sp_modify:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      node: "atlcdot-01"
      dhcp: "none"
      ip: "192.168.1.150"
      netmask: "255.255.255.0"
      gateway: "192.168.1.1"
      enabled: True

'''

def sp_modify(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  node = module.params['node']
  addr_family = module.params['addr_family']
  dhcp = module.params['dhcp']
  ip = module.params['ip']
  netmask = module.params['netmask']
  gateway = module.params['gateway']
  enabled = module.params['enabled']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("service-processor-network-modify")
  api.child_add_string("address-type", addr_family)
  api.child_add_string("dhcp", dhcp)
  api.child_add_string("node", node)
  api.child_add_string("ip-address", ip)
  api.child_add_string("netmask", netmask)
  api.child_add_string("gateway-ip-address", gateway)
  api.child_add_string("is-enabled", enabled)

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
      addr_family=dict(default='IPv4', choices=['IPv4', 'IPv6']),
      dhcp=dict(default='none', choices=['none', 'v4']),
      ip=dict(required=False, type='str'),
      netmask=dict(required=False, type='str'),
      gateway=dict(required=False, type='str'),
      enabled=dict(default=True, type='bool'),

    ),
    supports_check_mode = False
  )

  results = sp_modify(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




