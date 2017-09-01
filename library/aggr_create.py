#!/usr/bin/python

import sys
import json
from  ansible.module_utils import ntap_util

try:
    from NaServer import *
    NASERVER_AVAILABLE = True
except ImportError:
    NASERVER_AVAILABLE = False

if not NASERVER_AVAILABLE:
    module.fail_json(msg="The NetApp Manageability SDK library is not installed")

DOCUMENTATTION = '''
---
module: aggr_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create Aggregate NetApp CDOT
description:
  - Ansible module to create NetApp CDOT aggregates via the NetApp python SDK.

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
  node:
    required: True
    description:
      - "Name of node who owns the disks used to create the aggregate"
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
    required: True
    description:
      - "Disk size specified with the unit, e.g. 1024g|3t"    
  raid_size:
    required: True
    description:
      - "Maximum number of disks in each RAID group"
  raid_type:
    required: False
    description:
      - "Raid type."
    default: 'raid_dp'
    choices: ['raid4', 'raid_dp', 'raid_tec']

'''

EXAMPLES = '''
# Create Aggregate
- name: Create SSD Aggregate
    aggr_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      node: "atlcdot-01"
      act_disk_type: "SSD"
      aggr: "aggr0_ssd"
      disk_count: 23
      disk_size: 4t
      raid_size: 16
      raid_type: raid_dp

'''

def aggr_create(module):

    node = module.params['node']
    disk_type = module.params['disk_type']
    aggr = module.params['aggr']
    disk_count = module.params['disk_count']
    disk_size = module.params['disk_size']
    raid_size = module.params['raid_size']
    raid_type = module.params['raid_type']

    results = {}

    results['changed'] = False


    api = NaElement("aggr-create")
    api.child_add_string("disk-type", disk_type)
    api.child_add_string("aggregate", aggr)
    api.child_add_string("disk-count", disk_count)
    api.child_add_string("disk-size-with-unit", disk_size)
    api.child_add_string("raid-size", raid_size)
    api.child_add_string("raid-type", raid_type)

    xi = NaElement("nodes")
    api.child_add(xi)
    xi.child_add_string("node-name", node)

    connection = ntap_util.connect_to_api(module)
    xo = connection.invoke_elem(systemCli)

    if(xo.results_errno() != 0):
        r = xo.results_reason()
        module.fail_json(msg=r)
        results['changed'] = False

    else:
        results['changed'] = True

    return results

def main():

    argument_spec = ntap_util.ntap_argument_spec()
    argument_spec.update(dict(
        node=dict(required=True),
        disk_type=dict(required=True, type='str'),
        aggr=dict(required=True),
        disk_count=dict(required=True, type='int'),
        disk_size=dict(required=True, type='str'),
        raid_type=dict(default='raid_dp', type='str'),
        raid_size=dict(required=True, type='int'),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False) 

    results = aggr_create(module)

    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




