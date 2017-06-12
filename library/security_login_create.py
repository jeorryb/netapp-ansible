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
module: security_login_create
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Create a new user account on NetApp CDOT
description:
  - Ansible module to create a new user account on NetApp CDOT via the NetApp python SDK.

requirements: ["NetApp Manageability SDK"]

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
  login_user_name:
    required: True
    description:
      - "Name of the user. When creating a SNMPv1 or SNMPv2 user with 'snmp' application and 'community' authentication-method, the user name is the community string."
  login_password:
    required: False
    description:
      - "Password for the user account. This is ignored for creating snmp users. This is required for creating non-snmp users."
  application:
    required: True
    description:
      - "Name of the application. Possible values: 'console', 'http', 'ontapi', 'rsh', 'snmp', 'sp', 'ssh', 'telnet'."
  auth_method:
    required: True
    description:
      - "Authentication method for the application. Possible values: 'community', 'password', 'publickey', 'domain', 'nsswitch' and 'usm'."
  role:
    required: True
    description:
      - "Name of the role."

'''

EXAMPLES = '''
# Create user
- name: Create nagios user
    security_login_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      login_user_name: "nagios"
      login_user_name: "nagiosPassword1"
      application: "ontapi"
      auth_method: "password"
      role: "nagios"

'''

def security_login_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  login_user_name = module.params['login_user_name']
  login_password = module.params['login_password']
  application = module.params['application']
  auth_method = module.params['auth_method']
  role =  module.params['role']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("security-login-create")
  api.child_add_string("user-name", login_user_name)
  if module.params['login_password']:
    api.child_add_string("password", login_password)
  api.child_add_string("authentication-method", auth_method)
  api.child_add_string("application", application)
  api.child_add_string("role-name", role)
  api.child_add_string("vserver", vserver)

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
      login_user_name=dict(required=True, type='str'),
      login_password=dict(required=False),
      application=dict(required=True, choices=['console', 'http', 'ontapi', 'rsh', 'snmp', 'sp', 'ssh', 'telnet']),
      auth_method=dict(required=True, choices=['community', 'password', 'publickey', 'domain', 'nsswitch', 'usm']),
      role=dict(required=True, type='str'),

    ),
    supports_check_mode = False
  )

  results = security_login_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




