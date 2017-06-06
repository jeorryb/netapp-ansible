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
module: nfs_service_create
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Create NFS service on NetApp CDOT arrays
description:
  - Ansible module create a NFS service on NetApp CDOT arrays via the NetApp python SDK.
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
  nfs_access:
    required: False
    description:
      - "If 'true',then NFS server access is enabled. Default value is 'true'."
  nfsv3_enabled:
    required: False
    description:
      - "If 'true', then NFS version 3 is enabled. Default value is 'true'."
  nfsv40_enabled:
    required: False
    description:
      - "If 'true', then NFS version 4.0 is enabled. Default value is 'false'."
  nfsv41_enabled:
    required: False
    description:
      - "If 'true', then NFS version 4.1 is enabled. Default value is 'false'."
  nfsv41_pnfs_enabled:
    required: False
    description:
      - "If 'true', then Parallel NFS support for NFS version 4.1 is enabled. Default value is 'true'."
  vstorage_enabled:
    required: False
    description:
      - "If 'true', then enables the usage of vStorage protocol for server side copies, which is mostly used in hypervisors. Default value is 'false'."
    
'''

EXAMPLES = '''
# Create NFS Service
- name: Create NFS Service
    nfs_service_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      nfs_access: true
      nfsv3_enabled: true
      nfsv40_enabled: true
      nfsv41_enabled: true
      vstorage_enabled: true
      nfsv41_pnfs_enabled: true


'''

def nfs_service_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  nfs_access = module.params['nfs_access']
  nfsv3_enabled = module.params['nfsv3_enabled']
  nfsv40_enabled = module.params['nfsv40_enabled']
  nfsv41_enabled = module.params['nfsv41_enabled']
  vstorage_enabled = module.params['vstorage_enabled']
  nfsv41_pnfs_enabled = module.params['nfsv41_pnfs_enabled']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 15)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)
  s.set_vserver(vserver)

  api = NaElement("nfs-service-create")
  api.child_add_string("is-nfs-access-enabled", nfs_access)
  api.child_add_string("is-nfsv3-enabled", nfsv3_enabled)
  api.child_add_string("is-nfsv40-enabled", nfsv40_enabled)
  api.child_add_string("is-nfsv41-enabled", nfsv41_enabled)
  api.child_add_string("is-vstorage-enabled", vstorage_enabled)
  api.child_add_string("is-nfsv41-pnfs-enabled", nfsv41_pnfs_enabled)
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
      nfs_access=dict(required=False),
      nfsv3_enabled=dict(required=False),
      nfsv40_enabled=dict(required=False),
      nfsv41_enabled=dict(required=False),
      vstorage_enabled=dict(required=False),
      nfsv41_pnfs_enabled=dict(required=False),

    ),
    supports_check_mode = False
  )

  results = nfs_service_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




