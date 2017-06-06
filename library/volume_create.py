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
module: volume_create
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Create NetApp CDOT Volume
description:
  - Ansible module to create NetApp CDOT volumes via the NetApp python SDK.
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
  aggregate:
    required: False
    description:
      - "Flexible volumes only. The name of the aggregate in which to create the new flexible volume. If provided, this argument must be accompanied by the "size" parameter. This input is required for creating a Cluster-Mode volume."
  size:
    required: False
    description:
      - "Flexible volumes only. The initial size of the new flexible volume. The format to use is: < number > k|m|g|t where "k" means kilobytes, "m" means megabytes, "g" means gigabytes, and "t" means terabytes. If the trailing unit character doesn't appear, then < number > is interpreted as the number of bytes desired. If provided, this argument must be accompanied by the "aggregate" parameter."
  state:
    required: False
    description:
      - "Desired state of the volume after it is created. Possible values: online', 'restricted', 'offline'"
  type:
    required: False
    description:
      - "The type of the volume to be created. Possible values: "rw" - read-write volume (default setting), "ls" - load-sharing volume, "dp" - data-protection volume, "dc" - data-cache volume (FlexCache)"
  policy:
    required: False
    description:
      - "The name of the Export Policy to be used by NFS/CIFS protocols. The default policy name is 'default'."
  percentage_snapshot_reserve:
    required: False
    description:
      - "The percentage of disk space that has to be set aside as reserve for snapshot usage. The default value is 5. Range : [0..90]"
  junction_path:
    required: False
    description:
      - "The Junction Path at which this volume is to be mounted."
  snapshot_policy:
    required: False
    description:
      - "The name of the snapshot policy. The default policy name is 'default'."
  space_reserve:
    required: False
    description:
      - "Specifies the type of volume guarantee the new volume will use. Possible values: none, file, volume. If this argument is not provided, the default volume guarantee type is volume."
   
'''

EXAMPLES = '''
# Create a volume
- name: Creating a 150g volume named volume1
    volume_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      volume: "volume1"
      aggregate: "aggr0_ssd"
      junction_path: "/aggr0_ssd"
      percentage_snapshot_reserve: 0

'''

def volume_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  volume = module.params['volume']
  aggregate = module.params['aggregate']
  size = module.params['size']
  state = module.params['state']
  type = module.params['type']
  policy = module.params['policy']
  percentage_snapshot_reserve = module.params['percentage_snapshot_reserve']
  junction_path = module.params['junction_path']
  snapshot_policy = module.params['snapshot_policy']
  space_reserve = module.params['space_reserve']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 15)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)
  s.set_vserver(vserver)

  api = NaElement("volume-create")
  api.child_add_string("volume", volume)
  if module.params['aggregate']:
    api.child_add_string("containing-aggr-name", aggregate)
  if module.params['size']:
    api.child_add_string("size", size)
  if module.params['state']:
    api.child_add_string("volume-state", state)
  if module.params['type']:
    api.child_add_string("volume-type", type)
  if module.params['policy']:
    api.child_add_string("export-policy", policy)
  if module.params['percentage_snapshot_reserve']:
    api.child_add_string("percentage-snapshot-reserve", percentage_snapshot_reserve)
  if module.params['junction_path']:
    api.child_add_string("junction-path", junction_path)
  if module.params['snapshot_policy']:
    api.child_add_string("snapshot-policy", snapshot_policy)
  if module.params['space_reserve']:
    api.child_add_string("space-reserve", space_reserve)
  
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
      aggregate=dict(required=False, type='str'),
      size=dict(required=False),
      state=dict(required=False, choices=['online', 'restricted', 'offline']),
      type=dict(required=False, choices=['rw', 'ls', 'dp', 'dc']),
      policy=dict(required=False),
      percentage_snapshot_reserve=dict(required=False, type='int'),
      junction_path=dict(required=False),
      snapshot_policy=dict(required=False),
      space_reserve=dict(required=False, choices=['none', 'file', 'volume']),

    ),
    supports_check_mode = False
  )

  results = volume_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




