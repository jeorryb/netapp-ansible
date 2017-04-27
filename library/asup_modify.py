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
module: asup_modify
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Modify autosupport
description:
  - Ansible module to modify autosupport settings on NetApp CDOT arrays via the NetApp python SDK.
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
  val_certs:
    default: True
    description:
      - "Perform SSL certificate validation"
  from_addr:
    required: False
    description:
      - "sender of the autosupport message"
  is_node_subject:
    required: False
    description:
      - "Specifies whether the node name is included in the subject line"
  mail_host:
    required: False
    description:
      - "Name or IP of the smtp server to use"
  node:
    required: True
    description:
      - "Name of the node you are modifying"
  partner:
    required: False
    description:
      - "You can specify up to 5 partner vendor addresses"
  to_addr:
    required: False
    description:
      - "You can specify up to 5 recipient addresses"
  transport:
    required: False
    description:
      - "Name of transport protocol; smtp|http|https"
  enabled:
    required: False
    description:
      - "Specifies whether asup daemon is enabled"


'''

EXAMPLES = '''
# Modify ASUP
- name: Modify asup settings
    asup_modify:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      from_addr: "admin@widget.com"
      is_node_subject: True
      mail_host: "smtp.widget.com"
      node: "atlcdot-01"
      partner: "global@it.com"
      to_addr: "datacenter@widget.com"
      transport: "https"
      enabled: True

'''

def asup_modify(module):

    from_addr = module.params['from_addr']
    is_node_subject = module.params['is_node_subject']
    mail_host = module.params['mail_host']
    node = module.params['node']
    partner = module.params['partner']
    to_addr = module.params['to_addr']
    transport = module.params['transport']
    enabled = module.params['enabled']

    results = {}
    results['changed'] = False

    api = NaElement("autosupport-config-modify")
    api.child_add_string("node-name", node)

    if module.params['from_addr']:
        api.child_add_string("from", from_addr)

    if module.params['enabled']:
        api.child_add_string("is-enabled", enabled)

    if module.params['is_node_subject']:
        api.child_add_string("is-node-in-subject", is_node_subject)

    if module.params['mail_host']:
        xi3 = NaElement("mail-hosts")
        api.child_add(xi3)
        for smtp in mail_host:
            xi3.child_add_string("string", smtp)

    if module.params['partner']:
        xi1 = NaElement("partner-address")
        api.child_add(xi1)
        for addr in partner:
            xi1.child_add_string("mail-address", addr)

    if module.params['to_addr']:
        xi2 = NaElement("to")
        api.child_add(xi2)
        for addr in to_addr:
            xi2.child_add_string("mail-address", addr)

    if module.params['transport']:
        api.child_add_string("transport", transport)

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
        from_addr=dict(required=False),
        is_node_subject=dict(required=False, type='bool'),
        mail_host=dict(required=False, type='list'),
        node=dict(required=True),
        partner=dict(required=False, type='list'),
        to_addr=dict(required=False, type='list'),
        transport=dict(required=False, choices=['https', 'http', 'smtp']),
        enabled=dict(required=False, type='bool'),))

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False) 

    results = asup_modify(module)

    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




