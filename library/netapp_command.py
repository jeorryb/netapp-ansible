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
module: netapp_command
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Run a command on a NetApp cDOT array.
description:
  - Ansible module run any command on a NetApp CDOT array via the NetApp python SDK.
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
  command:
    required: True
    description:
      - "The command to be run"

'''

EXAMPLES = '''
# Run a command
- name: Modify the policy for the volume rootvol
    netapp_command:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      command: "volume modify -vserver vsm_nfs -volume rootvol -policy forbidden"

'''


def netapp_command(module):

    cluster = module.params['cluster']
    user_name = module.params['user_name']
    password = module.params['password']
    val_certs = module.params['val_certs']
    command = module.params['command']

    connection = NaServer(cluster, 1 , 0)
    connection.set_server_type("FILER")
    connection.set_transport_type("HTTPS")
    connection.set_port(443)
    connection.set_style("LOGIN")
    connection.set_admin_user(user_name, password)

    if not val_certs:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        
        except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
        # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context

    results = {}

    results['changed'] = False


    args = NaElement("args")
    command_list=command.split()
    for cmd in command_list:
      args.child_add(NaElement("arg", cmd))


    systemCli = NaElement("system-cli")
    systemCli.child_add(args)
    xo = connection.invoke_elem(systemCli)

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
      command=dict(required=True, type='str'),
    ), 
      supports_check_mode=False
  )
  results = netapp_command(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import * 
main()




