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

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  domains = module.params['domains']
  dns_servers = module.params['dns_servers']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

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
  xo = s.invoke_elem(systemCli)

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
      domains=dict(required=True),
      dns_servers=dict(required=True),
    ),
    supports_check_mode = False
  )

  results = dns_create(module)



  module.exit_json(**results)

from ansible.module_utils.basic import *
main()
