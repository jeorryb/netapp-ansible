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
module: aggr_rename
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Rename NetApp CDOT Aggregate
description:
  - Ansible module to rename NetApp CDOT aggregates via the NetApp python SDK.
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
      - "Name of the aggregate you want to rename"
  new_aggr_name:
    required: True
    description:
      - "New name for the aggregate"
'''

EXAMPLES = '''
# Rename aggregate
- name: Rename aggregate
    aggr_rename:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      aggr: "old_aggregate"
      new_aggr_name: "my_new_aggr0"

'''

def aggr_rename(module):

    aggr = module.params['aggr']
    new_aggr_name = module.params['new_aggr_name']

    results = {}
    results['changed'] = False

    api = NaElement("aggr-rename")
    api.child_add_string("aggregate", aggr)
    api.child_add_string("new-aggregate-name", new_aggr_name)
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
        aggr=dict(required=True),
        new_aggr_name=dict(required=True),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = aggr_rename(module)



    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




