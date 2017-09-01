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
module: failover_group_create
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Create a failover group
description:
  - Ansible module to create a failover group on NetApp CDOT arrays via the NetApp python SDK.
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
  failover_group:
    required: True
    description:
      - "The failover group name."
  return_record:
    required: False
    description:
      - "If set to true, returns the Failover Group on successful creation. Default: false"
  targets:
    required: True
    description:
      - "The list of potential failover targets to be used. Lifs within the specified vserver and assigned to the specified failover-group will use this list of failover targets as needed. Format: node-name:port-name"
  vserver:
    results: True
    description:
      - "The vserver for which the failover group is defined."


'''

EXAMPLES = '''
# Create a failover group
- name: Create cluster-mgmt failover group
    failover_group_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      failover_group: "cluster-mgmt"
      targets: ["atlcdot-01:e0d", "atlcdot-02:e0d"]
      vserver: "cluster-vserver"

'''

def failover_group_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  failover_group = module.params['failover_group']
  return_record = module.params['return_record']
  targets = module.params['targets']
  vserver = module.params['vserver']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("net-failover-group-create")
  api.child_add_string("failover-group", failover_group)
  if module.params['return_record']:
    api.child_add_string("ipspace", ipspace)
  api.child_add_string("vserver", vserver)

  xi = NaElement("targets")
  api.child_add(xi)

  for target in targets:
    xi.child_add_string("net-qualified-port-name", target)

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
      failover_group=dict(required=True, type='str'),
      return_record=dict(required=False, type='bool'),
      targets=dict(required=True, type='list'),
      vserver=dict(required=True, type='str'),

    ),
    supports_check_mode = False
  )

  results = failover_group_create(module)



  module.exit_json(**results)

from ansible.module_utils.basic import *
main()
