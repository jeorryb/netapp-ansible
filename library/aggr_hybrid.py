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
module: aggr_hybrid
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Modify aggregate to be a flash pool
description:
  - Ansible module to modify existing NetApp CDOT aggregate to allow SSDs and become a flash pool via the NetApp python SDK.
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
  aggr:
    required: True
    description:
      - "Name of aggregate"
  hybrid:
    required: True
    description:
      - "Boolean to enable or disable hybrid aggregate"
    default: True

'''

EXAMPLES = '''
# Create flashpool
- name: Change aggr0 to hybrid_enabled true
    aggr_hybrid:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      aggr: "aggr0_ssd"
      hybrid: "True"

'''

def aggr_hybrid(module):

    aggr = module.params['aggr']
    hybrid = module.params['hybrid']

    results = {}

    results['changed'] = False

    args = NaElement("args")

    args.child_add(NaElement("arg", "aggregate"))
    args.child_add(NaElement("arg", "modify"))
    args.child_add(NaElement("arg", aggr))
    args.child_add(NaElement("arg", "-hybrid-enabled"))
    args.child_add(NaElement("arg", hybrid))

    systemCli = NaElement("system-cli")
    systemCli.child_add(args)
    connection = ntap_util.connect_to_api(module)
    xo = connection.invoke_elem(systemCli)

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
        aggr=dict(required=True),
        hybrid=dict(default=True, type='bool'),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    results = aggr_hybrid(module)

    module.exit_json(**results)

from ansible.module_utils.basic import *
main()



