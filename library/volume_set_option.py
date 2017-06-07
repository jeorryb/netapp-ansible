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
module: volume_set_option
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Configure options on a NetApp CDOT Volume
description:
  - Ansible module to set options on NetApp CDOT volumes via the NetApp python SDK.
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
      - "Name of the volume to create. The volume name can contain letters, numbers, and the underscore character (_), but the first character must be a letter or an underscore. In Data ONTAP Cluster-Mode, the volume names must be unique within a Vserver."
  option_name:
    required: True
    description:
      - "Name of the option to be set."
  option_value:
    required: True
    description:
      - "The value to set the named option (except for option 'root', which has no associated value)."
  
'''

EXAMPLES = '''
# Set an option on a volume
- name: Setting fractional_reserve on volume1
    volume_set_option:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      volume: "volume1"
      option_name: "fractional_reserve"
      option_value: "0%"

'''

def volume_set_option(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  volume = module.params['volume']
  option_name = module.params['option_name']
  option_value = module.params['option_value']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 15)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)
  s.set_vserver(vserver)

  api = NaElement("volume-set-option")
  api.child_add_string("volume", volume)
  api.child_add_string("option-name", option_name)
  api.child_add_string("option-value", option_value)
 
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
      volume=dict(required=True, type='str'),
      option_name=dict(required=True, type='str'),
      option_value=dict(required=True, type='str'),

    ),
    supports_check_mode = False
  )

  results = volume_set_option(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




