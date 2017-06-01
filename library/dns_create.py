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
module: dns_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Set date, time and timezone for NetApp cDOT array.
description:
  - Ansible module to create dns server entries for a NetApp CDOT array via the NetApp python SDK.
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
      - "vserver that DNS entries are being created on"
  domains:
    required: True
    description:
      - "Comma separated list of domains (FQDN) that the servers are responsible for"
  dns_servers:
    required: True
    description:
      - "Comma separated list of dns servers"

'''

EXAMPLES = '''
# Create DNS servers for cluster vserver
- name: Create dns servers
    dns_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "atlcdot"
      domains: "netapp.com"
      dns_servers: "8.8.8.8, 4.2.2.2"

'''


def dns_create(module):

    domains = module.params['domains']
    dns_servers = module.params['dns_servers']
    vserver = module.params['vserver']

    results = {}
    results['changed'] = False

    args = NaElement("args")

    args.child_add(NaElement("arg", "dns"))
    args.child_add(NaElement("arg", "create"))
    args.child_add(NaElement("arg", "-vserver"))
    args.child_add(NaElement("arg", vserver))
    args.child_add(NaElement("arg", "-domains"))
    args.child_add(NaElement("arg", domains))
    args.child_add(NaElement("arg", "-name-servers"))
    args.child_add(NaElement("arg", dns_servers))

    systemCli = NaElement("system-cli")
    systemCli.child_add(args)
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
        domains=dict(required=True),
        vserver=dict(required=True),
        dns_servers=dict(required=True),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = dns_create(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()
