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
module: license_add
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Add licenses to NetApp cDOT array
description:
  - Ansible module to add licenses to a NetApp CDOT array via the NetApp python SDK.
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
  license_keys:
    required: True
    description:
      - "List of license keys you want to add"

'''

EXAMPLES = '''
# Add License Keys
- name: Add License Keys
    license_add:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      license_keys: [aaaaaaaaa, bbbbbbbbbbb, ccccccccc]

'''

def license_add(module):

    license_keys = module.params['license_keys']

    results = {}
    results['changed'] = False

    api = NaElement("license-v2-add")
    xi = NaElement("codes")

    api.child_add(xi)

    for key in license_keys:
        xi.child_add_string("license-code-v2", key)

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
        license_keys=dict(required=True, type='list'),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = license_add(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




