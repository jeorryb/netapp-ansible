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
module: asup_invoke
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Invoke AutoSupport
description:
  - Ansible module to invoke AutoSupport for NetApp CDOT arrays via the NetApp python SDK.
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
      - "Name of the node on which the autosupport message will be generated"
  message:
    required: False
    description:
      - "Text to include as part of the AutoSupport email subject line"
  asup_type:
    required: True
    description:
      - "Type of autosupport to generate"
    default: 'all'
    choices: ['test', 'performance', 'all']
  uri:
    required: False
    description:
      - "Alternate destination for the autosupport message"


'''

EXAMPLES = '''
# Send ASUP
- name: Send asup prior to upgrade
    asup_invoke:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      node: "atlcdot-01"
      message: "Beginning upgrade to 9.0"
      asup_type: "all"

'''

def asup_invoke(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  node = module.params['node']
  message = module.params['message']
  asup_type = module.params['asup_type']
  uri = module.params['uri']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("autosupport-invoke")
  api.child_add_string("node-name", node)
  api.child_add_string("type", asup_type)

  if module.params['message']:
    api.child_add_string("message", message)

  if module.params['uri']:
    api.child_add_string("uri", uri)


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
      message=dict(required=False),
      asup_type=dict(default="all", choices=['test', 'performance', 'all']),
      uri=dict(required=False),

    ),
    supports_check_mode = False
  )

  results = asup_invoke(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




