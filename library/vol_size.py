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
module: vol_size
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Resize NetApp CDOT Volume
description:
  - Ansible module to resize NetApp CDOT volumes via the NetApp python SDK.
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
  volume:
    required: True
    description:
      - "Name of the volume you want to resize"
  size:
    required: True
    description:
      - "New size for the volume"
'''

EXAMPLES = '''
# Resize Volume
- name: Resize volume
    vol_size:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      volume: "documents"
      size: "2tb"

'''

def vol_size(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  volume = module.params['volume']
  size = module.params['size']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 15)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)
  s.set_vserver(vserver)

  api = NaElement("volume-size")
  api.child_add_string("volume",volume)
  api.child_add_string("new-size",size)
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
      volume=dict(required=True),
      size=dict(required=True),
    ),
    supports_check_mode = False
  )

  results = vol_size(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




