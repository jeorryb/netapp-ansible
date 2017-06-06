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
module: snmp_community_add
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Configure SNMP on NetApp CDOT Arrays
description:
  - Ansible module to configure the community of SNMP on NetApp CDOT Arrays via the NetApp python SDK.
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
  access_control:
    required: True
    description:
      - "Access control for the community. Possible values are "ro" (read-only) and "rw" (read-write). But, only "ro" (read-only) communities are supported."
  community:
    required: True
    description:
      - "Community name to be added."
   
'''

EXAMPLES = '''
# Configuring SNMP
- name: Setting SNMP Community to public
    snmp_community_add:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      access_control: "ro"
      community: "public"

'''

def snmp_community_add(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  access_control = module.params['access_control']
  community = module.params['community']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 15)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)
  s.set_vserver(vserver)

  api = NaElement("snmp-community-add")
  api.child_add_string("access-control", access_control)
  api.child_add_string("community", community)
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
      access_control=dict(required=False, choices=['ro', 'rw']),
      community=dict(required=False),

    ),
    supports_check_mode = False
  )

  results = snmp_community_add(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




