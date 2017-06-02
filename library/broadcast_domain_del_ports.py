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
module: broadcast_domain_del_ports
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Del ports from broadcast domain
description:
  - Ansible module to del ports from a broadcast domain on NetApp CDOT arrays via the NetApp python SDK.
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
  ipspace:
    required: True
    description:
      - "IPspace name that the layer 2 broadcast domain belongs to; eg. 'Default'"
  bc_domain:
    required: True
    description:
      - "Name of the broadcast domain"
  ports:
    required: True
    description:
      - "List of ports that will be added to the broadcast domain; Format node_name:port_name"


'''

EXAMPLES = '''
# Remove ports from default broadcast domain
- name: Remove e0c & e0d from broadcast domain Default
    broadcast_domain_del_ports:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      ipspace: "Default"
      bc_domain: "Default"
      ports: ["atlcdot-01:e0d", "atlcdot-02:e0d"]

'''

def broadcast_domain_remove_ports(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  ipspace = module.params['ipspace']
  bc_domain = module.params['bc_domain']
  ports = module.params['ports']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("net-port-broadcast-domain-remove-ports")
  api.child_add_string("broadcast-domain", bc_domain)
  api.child_add_string("ipspace", ipspace)

  xi = NaElement("ports")
  api.child_add(xi)

  for port in ports:
    xi.child_add_string("net-qualified-port-name", port)

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
      ipspace=dict(required=True),
      bc_domain=dict(required=True),
      ports=dict(required=True, type='list'),

    ),
    supports_check_mode = False
  )

  results = broadcast_domain_remove_ports(module)



  module.exit_json(**results)

from ansible.module_utils.basic import *
main()
