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
module: ntp_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create ntp server
description:
  - Ansible module to create ntp server for  NetApp CDOT via the NetApp python SDK.
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
  ntp_server:
    required: True
    description:
      - "Name or IP of the time server you wish to use"
  
'''

EXAMPLES = '''
# Create ntp server
- name: Create ntp server
    ntp_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      ntp_server: "tick.gatech.edu"

'''

def ntp_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  ntp_server = module.params['ntp_server']
  

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("ntp-server-create")
  api.child_add_string("server-name", ntp_server)
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
      ntp_server=dict(required=True),
    ),
    supports_check_mode = False
  )

  results = ntp_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




