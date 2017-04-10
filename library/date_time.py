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
module: date_time
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Set date, time and timezone for NetApp cDOT array.
description:
  - Ansible module to set the date, time and timezone for a NetApp CDOT array via the NetApp python SDK.
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
  timezone:
    required: False
    description:
      - "Timezone specified in the Olson format, Area/Location Timezone"
  date:
    required: True
    description:
      - "This sets the date and time, in the format MM/DD/YYYY HH:MM:SS"

'''

EXAMPLES = '''
# Change date and timezone
- name: Change date and timezone
    date_time:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      timezone: "America\New_York"
      date: "09/01/2016 10:26:00"

'''


def date_time(module):

    cluster = module.params['cluster']
    user_name = module.params['user_name']
    password = module.params['password']
    val_certs = module.params['val_certs']
    timezone = module.params['timezone']
    date = module.params['date']

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

    args.child_add(NaElement("arg", "cluster"))
    args.child_add(NaElement("arg", "date"))
    args.child_add(NaElement("arg", "modify"))
    if module.params['timezone']:
        args.child_add(NaElement("arg", "-timezone"))
        args.child_add(NaElement("arg", timezone))
    if module.params['date']:
        args.child_add(NaElement("arg", "-date"))
        args.child_add(NaElement("arg", date))

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
      timezone=dict(required=False),
      date=dict(required=True),
    ), 
      supports_check_mode=False
  )
  results = date_time(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import * 
main()




