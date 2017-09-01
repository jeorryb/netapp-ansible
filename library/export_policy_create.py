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
module: export_policy_create
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Create an export policy on a NetApp CDOT vserver
description:
  - Ansible module to create an export policy NetApp CDOT vserver via the NetApp python SDK.
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
  vserver:
    required: True
    description:
      - "name of the vserver"
  policy_name:
    required: True
    description:
      - "Export policy name."
  return_record:
    required: False
    description:
      - "If set to true, returns the Export policy configuration. on successful creation. Default: false"
   
'''

EXAMPLES = '''
# Create Export Policy
- name: Create forbidden export policy
    export_policy_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      policy_name: "forbidden"


'''

def export_policy_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  policy_name = module.params['policy_name']
  return_record = module.params['return_record']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 15)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)
  s.set_vserver(vserver)

  api = NaElement("export-policy-create")
  api.child_add_string("policy-name", policy_name)
  if module.params['return_record']:
    api.child_add_string("return-record", return_record)
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
      vserver=dict(required=True),
      policy_name=dict(required=True),
      return_record=dict(required=False, type='bool'),

    ),
    supports_check_mode = False
  )

  results = export_policy_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




