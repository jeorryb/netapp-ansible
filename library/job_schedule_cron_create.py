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
module: job_schedule_cron_create
version_added: "1.0"
author: "Valerian Beaudoin"
short_description: Create a new cron job schedule entry on NetApp CDOT
description:
  - Ansible module to create a new cron job schedule entry on NetApp CDOT via the NetApp python SDK.

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
  name:
    required: True
    description:
      - "The name of the job schedule."
  day:
    required: False
    description:
      - "The day(s) of the month when the job should be run."
  day_of_week:
    required: False
    description:
      - "The day(s) in the week when the job should be run."
  hour:
    required: False
    description:
      - "The hour(s) of the day when the job should be run."
  minute:
    required: False
    description:
      - "The minute(s) of each hour when the job should be run."
  month:
    required: False
    description:
      - "The month(s) when the job should be run."

'''

EXAMPLES = '''
# Create schedule
- name: Create daily4AM schedule
    job_schedule_cron_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      name: "daily4AM"
      hour: ["4"]
      minute: ["0"]

'''

def job_schedule_cron_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  name = module.params['name']
  day = module.params['day']
  day_of_week = module.params['day_of_week']
  hour = module.params['hour']
  minute = module.params['minute']
  month = module.params['month']

  results = {}

  results['changed'] = False

  s = NaServer(cluster, 1 , 0)
  s.set_server_type("FILER")
  s.set_transport_type("HTTPS")
  s.set_port(443)
  s.set_style("LOGIN")
  s.set_admin_user(user_name, password)

  api = NaElement("job-schedule-cron-create")
  api.child_add_string("job-schedule-name", name)
  if module.params['day']:
    xi = NaElement("job-schedule-cron-day")
    api.child_add(xi)
    for d in day:
      xi.child_add_string("cron-day-of-month", d)
  if module.params['day_of_week']:
    xi = NaElement("job-schedule-cron-day-of-week")
    api.child_add(xi)
    for dow in day_of_week:
      xi.child_add_string("cron-day-of-week", dow)
  if module.params['hour']:
    xi = NaElement("job-schedule-cron-hour")
    api.child_add(xi)
    for h in hour:
      xi.child_add_string("cron-hour", h)
  if module.params['minute']:
    xi = NaElement("job-schedule-cron-minute")
    api.child_add(xi)
    for min in minute:
      xi.child_add_string("cron-minute", min)
  if module.params['month']:
    xi = NaElement("job-schedule-cron-month")
    api.child_add(xi)
    for m in month:
      xi.child_add_string("cron-month", m)


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
      name=dict(required=True, type='str'),
      day=dict(required=False, type='list'),
      day_of_week=dict(required=False, type='list'),
      hour=dict(required=False, type='list'),
      minute=dict(required=False, type='list'),
      month=dict(required=False, type='list'),

    ),
    supports_check_mode = False
  )

  results = job_schedule_cron_create(module)

  

  module.exit_json(**results)

from ansible.module_utils.basic import *
main()




