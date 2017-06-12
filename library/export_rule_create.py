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
module: export_rule_create
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Create an export rule on a NetApp CDOT vserver
description:
  - Ansible module to create an export rule NetApp CDOT vserver via the NetApp python SDK.
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
  client_match:
    required: False
    description:
      - "Client match specification for Export rule. The clients specified are enforced with this Export rule. The rule with the higher rule index value takes precedence."
  ro_rule:
    required: False
    description:
      - "Rule for read-only access. Possible values: 'any', 'none', 'never', 'krb5', 'ntlm', 'sys', 'spinauth'"
  rw_rule:
    required: False
    description:
      - "Rule for read-write access. Possible values: 'any', 'none', 'never', 'krb5', 'ntlm', 'sys', 'spinauth'"
  protocol:
    required: False
    description:
      - "Client access protocol. Default value is 'any'. Possible values: 'any', 'nfs2', 'nfs3', 'nfs3', 'cifs', 'nfs4', 'flexcache'"
  super_user_security:
    required: False
    description:
      - "Security flavors for the superuser. Default value is 'none'. Possible values: 'any', 'none', 'never', 'krb5', 'ntlm', 'sys', 'spinauth'"
  rule_index:
    required: False
    description:
      - "Export rule index. A next available value is assigned if no value is provided during create else the rule is inserted at the given rule index position in the export-rule table."
  allow_suid:
    required: False
    description:
      - "If 'true', NFS server will honor SetUID bits in SETATTR operation. Default value is 'true'."

   
'''

EXAMPLES = '''
# Create Export rule
- name: Create rule associated to forbidden export policy
    export_rule_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      policy_name: "forbidden"
      client_match: "0.0.0.0/0"
      ro_rule: ["none"]
      rw_rule: ["none"]
      protocol: ["nfs, cifs"]


'''

def export_rule_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  policy_name = module.params['policy_name']
  client_match = module.params['client_match']
  ro_rule = module.params['ro_rule']
  rw_rule = module.params['rw_rule']
  protocol = module.params['protocol']
  super_user_security = module.params['super_user_security']
  rule_index = module.params['rule_index']
  allow_suid = module.params['allow_suid']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 15)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)
  s.set_vserver(vserver)

  api = NaElement('export-rule-create')
  api.child_add_string('policy-name', policy_name)
  api.child_add_string('client-match', client_match)
  if module.params['ro_rule']:
    xi = NaElement('ro-rule')
    api.child_add(xi)
    for flavor in ro_rule:
      xi.child_add_string('security-flavor', flavor)
  if module.params['rw_rule']:
    xi = NaElement("rw-rule")
    api.child_add(xi)
    for flavor in rw_rule:
      xi.child_add_string("security-flavor", flavor)
  if module.params['protocol']:
    xi = NaElement('protocol')
    api.child_add(xi)
    for proto in protocol:
      xi.child_add_string('access-protocol', proto)
  if module.params['super_user_security']:
    xi = NaElement('super-user-security')
    api.child_add(xi)
    for flavor in super_user_security:
      xi.child_add_string('security-flavor', flavor)
  if module.params['rule_index']:
    api.child_add_string('rule-index', rule_index)
  if module.params['allow_suid']:
    api.child_add_string('is-allow-set-uid-enabled', allow_suid)
  
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
      client_match=dict(required=True, type='str'),
      ro_rule=dict(required=False, type='list'),
      rw_rule=dict(required=False, type='list'),
      protocol=dict(required=False, type='list'),
      super_user_security=dict(required=False, type='list'),
      rule_index=dict(required=False, type='int'),
      allow_suid=dict(required=False, type='bool'),

    ),
    supports_check_mode = False
  )

  results = export_rule_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




