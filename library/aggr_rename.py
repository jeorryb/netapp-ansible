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
module: aggr_rename
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Rename NetApp CDOT Aggregate
description:
  - Ansible module to rename NetApp CDOT aggregates via the NetApp python SDK.
requirements:
  - NetApp Manageability SDK
options:
  node:
    required: True
    description:
      - "The ip address or hostname of the node"
  user_name:
    required: True
    description:
      - "Administrator user for the cluster/node"
  password:
    required: True
    description:
      - "password for the admin user"
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
      node: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      aggr: "old_aggregate"
      new_aggr_name: "my_new_aggr0"

'''

def aggr_rename(module):

	node = module.params['node']
	user_name = module.params['user_name']
	password = module.params['password']
	aggr = module.params['aggr']
	new_aggr_name = module.params['new_aggr_name']

	results = {}

	results['changed'] = False

	s = NaServer(node, 1 , 30)
	s.set_server_type("FILER")
	s.set_transport_type("HTTPS")
	s.set_port(443)
	s.set_style("LOGIN")
	s.set_admin_user(user_name, password)

	api = NaElement("aggr-rename")
	api.child_add_string("aggregate",aggr)
	api.child_add_string("new-aggregate-name",new_aggr_name)
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
			node=dict(required=True),
			user_name=dict(required=True),
			password=dict(required=True),
			aggr=dict(required=True),
			new_aggr_name=dict(required=True),
		),
		supports_check_mode = False
	)

	results = aggr_rename(module)

	

	module.exit_json(**results)

from ansible.module_utils.basic import *
main()




