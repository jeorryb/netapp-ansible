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
module: int_modify
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Create interface
description:
  - Ansible module to create interfaces on NetApp CDOT arrays via the NetApp python SDK.
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
      - "vserver name"
  lif:
    required: True
    description:
      - "name of the logical interface"
  role:
    required: False
    description:
      - "specifies the role of the LIF"
  data_proto:
    required: False
    description:
      - "Specifies the list of data protocols specified on the LIF"
  node:
    required: False
    description:
      - "Home node of the LIF"
  port:
    required: False
    description:
      - "Home port of the LIF"
  ip:
    required: False
    description:
      - "IP address of the LIF"
  netmask:
    required: False
    description:
      - "Subnet mask of the LIF"
  subnet:
    required: False
    description:
      - "subnet name; ip and netmask not used if this parameter is specified"
  failover_group:
    required: False
    description:
      - "Specifies the failover group name."
  failover_policy:
    required: False
    description:
      - "Specifies the failover policy for the LIF. Possible values: 'nextavail', 'priority', 'disabled', 'system_defined', 'system_defined', 'sfo_partner_only', 'ipspace_wide', 'broadcast_domain_wide'"


'''

EXAMPLES = '''
# Modify failover for lif lif_nfs_01
- name: change failover to system-defined and cluster-mgmt
    int_modify:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      lif: "lif_nfs_01"
      failover_group: "cluster-mgmt"
      failover_policy: "system_defined"

'''

def int_modify(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  node = module.params['node']
  vserver = module.params['vserver']
  lif = module.params['lif']
  role = module.params['role']
  data_proto = module.params['data_proto']
  port = module.params['port']
  ip = module.params['ip']
  netmask = module.params['netmask']
  subnet = module.params['subnet']
  failover_group = module.params['failover_group']
  failover_policy = module.params['failover_policy']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement('net-interface-modify')

  if module.params['ip']:
    api.child_add_string('address', ip)
  if module.params['data_proto']:
    xi = NaElement('data-protocols')
    api.child_add(xi)
    for proto in data_proto:
      xi.child_add_string('data-protocol', proto)
  if module.params['node']:
    api.child_add_string('home-node', node)
  if module.params['port']:
    api.child_add_string('home-port', port)
  api.child_add_string('interface-name', lif)
  if module.params['netmask']:
    api.child_add_string('netmask', netmask)
  if module.params['node']:
    api.child_add_string('role', role)
  api.child_add_string('vserver', vserver)
  if module.params['subnet']:
    api.child_add_string('subnet-name', subnet)
  if module.params['failover_group']:
    api.child_add_string('failover-group', failover_group)
  if module.params['failover_policy']:
    api.child_add_string('failover-policy', failover_policy)



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
      node=dict(required=False),
      vserver=dict(required=True),
      lif=dict(required=True),
      role=dict(required=False, choices=['undef', 'cluster', 'data', 'node_mgmt', 'intercluster', 'cluster_mgmt']),
      data_proto=dict(required=False, type='list'),
      port=dict(required=False),
      ip=dict(required=False),
      netmask=dict(required=False),
      subnet=dict(required=False),
      failover_group=dict(required=False),
      failover_policy=dict(required=False, choices=['nextavail', 'priority', 'disabled', 'system_defined', 'system_defined', 'sfo_partner_only', 'ipspace_wide', 'broadcast_domain_wide']),

    ),
    supports_check_mode = False
  )

  results = int_modify(module)



  module.exit_json(**results)

from ansible.module_utils.basic import *
main()
