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
module: aggr_add
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Add disks to Aggregate NetApp CDOT
description:
  - Ansible module to add disks to an existing NetApp CDOT aggregate via the NetApp python SDK.

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
  disk_type:
    required: True
    description:
      - "Actual disk type of disks used for aggregate."
    choices: ['ATA', 'BSAS', 'FCAL', 'FSAS', 'LUN', 'MSATA', 'SAS', 'SSD', 'VMDISK']
  aggr:
    required: True
    description:
      - "Name of aggregate"
  disk_count:
    required: True
    description:
      - "Number of disks used to create the aggregate"
  disk_size:
    required: False
    description:
      - "Size of disks to add specified with the unit of measurements; e.g. 2048g|3t"

'''

EXAMPLES = '''
# Add disks to Aggregate
- name: Add disks to SSD Aggregate
    aggr_add:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      disk_type: "SSD"
      aggr: "aggr0_ssd"
      disk_count: 12
      disk_size: 2048g

'''

def aggr_add(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  disk_type = module.params['disk_type']
  aggr = module.params['aggr']
  disk_count = module.params['disk_count']
  disk_size = module.params['disk_size']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("aggr-add")
  api.child_add_string("disk-type", disk_type)
  api.child_add_string("aggregate", aggr)
  api.child_add_string("disk-count", disk_count)
  api.child_add_string("disk-size-with-unit", disk_size)


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
      disk_type=dict(required=True, type='str'),
      aggr=dict(required=True),
      disk_count=dict(required=True, type='int'),
      disk_size=dict(required=True, type='str'),

    ),
    supports_check_mode = False
  )

  results = aggr_add(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




