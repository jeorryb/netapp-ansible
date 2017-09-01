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
module: storage_pool_create
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Create Storage Pool NetApp CDOT
description:
  - Ansible module to create storage pools to a NetApp CDOT via the NetApp python SDK.

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
  val_certs:
    default: True
    description:
      - "Perform SSL certificate validation"
  disk_list:
    required: True
    description:
      - "List of disks used for the storage pool."
  storage_pool:
    required: True
    description:
      - "Name of the storage pool"
  simulate:
    required: False
    default: False
    description:
      - "Simulate the creation of storage pool."

'''

EXAMPLES = '''
# Create Storage Pool
- name: Create flashpool with 3 SSDs
    storage_pool_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      storage_pool: "flashpool01"
      disk_list: ["1.0.0","1.0.1","1.0.2"]

'''

def storage_pool_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  val_certs = module.params['val_certs']
  disk_list = module.params['disk_list']
  storage_pool = module.params['storage_pool']
  simulate = module.params['simulate']

  results = {}

  results['changed'] = False

  if not val_certs:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        
        except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
        # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("storage-pool-create")
  api.child_add_string("storage-pool", storage_pool)
  if module.params['simulate']:
    api.child_add_string("simulate", simulate)

  xi = NaElement("disk-list")
  api.child_add(xi)

  for disk in disk_list:
    xi.child_add_string("disk-name", disk)

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
      val_certs=dict(type='bool', default=True),
      storage_pool=dict(required=True, type='str'),
      disk_list=dict(required=True, type='list'),
      simulate=dict(required=False, type='bool'),

    ),
    supports_check_mode = False
  )

  results = storage_pool_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()

