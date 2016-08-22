#!/usr/bin/python

DOCUMENTATION = '''
---
module: sp_modify
version_added: 0.1
short_description: service-processor modify
description:
  - modify IP network settings for a NetApp cluster node service-processor
  '''

  import sys
  import json
  from NaServer import *

  EXAMPLES = '''
  EXAMPLES
  '''

  def sp_modify(module):
  	