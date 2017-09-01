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
  val_certs:
    default: True
    description:
      - "Perform SSL certificate validation"
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

    node = module.params['node']
    message = module.params['message']
    asup_type = module.params['asup_type']
    uri = module.params['uri']

    results = {}
    results['changed'] = False

    api = NaElement("autosupport-invoke")
    api.child_add_string("node-name", node)
    api.child_add_string("type", asup_type)

    if module.params['message']:
        api.child_add_string("message", message)

    if module.params['uri']:
        api.child_add_string("uri", uri)

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
        message=dict(required=False),
        asup_type=dict(default="all", choices=['test', 'performance', 'all']),
        uri=dict(required=False),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = asup_invoke(module)

    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




