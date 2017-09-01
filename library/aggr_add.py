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
module: aggr_add
version_added: "1.1"
author: "Jeorry Balasabas (@jeorryb) & Valerian Beaudoin"
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
  val_certs:
    default: True
    description:
      - "Perform SSL certificate validation"
  disk_type:
    required: False
    description:
      - "Actual disk type of disks used for aggregate."
    choices: ['ATA', 'BSAS', 'FCAL', 'FSAS', 'LUN', 'MSATA', 'SAS', 'SSD', 'VMDISK']
  aggr:
    required: True
    description:
      - "Name of aggregate"
  disk_count:
    required: False
    description:
      - "Number of disks used to create the aggregate"
  disk_size:
    required: False
    description:
      - "Size of disks to add specified with the unit of measurements; e.g. 2048g|3t"
  storage_pool:
    required: False
    description:
      - "Name of the storage pool from which the capacity will be added. This parameter cannot be used with disk-list or disk-count option."
  allocation_units:
    required: False
    description:
      - "The spare capacity in terms of number of allocation units to be added to a given aggregate. This option works only when 'storage-pool' is specified."
  raid_type:
    required: False
    description:
      - "Specifies the raid-type of the new RAID groups being created as part of the disk add operation. This option should be used while adding SSD disks for the first time to a hybrid-enabled aggregate. Possible values: raid4 and raid_dp only. If not specified, the default value is the raid-type of the aggregate."

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


    disk_type = module.params['disk_type']
    aggr = module.params['aggr']
    disk_count = module.params['disk_count']
    disk_size = module.params['disk_size']
    storage_pool = module.params['storage_pool']
    allocation_units = module.params['allocation_units']
    raid_type = module.params['raid_type']

    results = {}

    results['changed'] = False

    api = NaElement("aggr-add")
    if module.params['disk_type']:
        api.child_add_string("disk-type", disk_type)
    api.child_add_string("aggregate", aggr)
    if module.params['disk_count']:
        api.child_add_string("disk-count", disk_count)
    if module.params['disk_size']:
        api.child_add_string("disk-size-with-unit", disk_size)
    if module.params['storage_pool']:
        api.child_add_string("storage-pool", storage_pool)
    if module.params['allocation_units']:
        api.child_add_string("allocation-units", allocation_units)
    if module.params['raid_type']:
        api.child_add_string("cache-raid-type", raid_type)


    connection = ntap_util.connect_to_api(module)
    xo = connection.invoke_elem(api)

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
    disk_type=dict(required=False, type='str'),
    aggr=dict(required=True),
    disk_count=dict(required=False, type='int'),
    storage_pool=dict(required=False, type='str'),
    allocation_units=dict(required=False, type='int'),
    raid_type=dict(required=False, type='str'),
    disk_size=dict(required=False, type='str'),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = aggr_add(module)


  
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()

