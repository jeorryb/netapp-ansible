import sys
from NaServer import *

s = NaServer('n4m', 1, 0)
s.set_server_type("FILER")
s.set_transport_type("HTTPS")
s.set_port(443)
s.set_style("LOGIN")
s.set_admin_user('admin', 'netapp123')

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

args = NaElement("args")

args.child_add(NaElement("arg", "cluster"))
args.child_add(NaElement("arg", "date"))
args.child_add(NaElement("arg", "modify"))
#   if module.params['timezone']:
args.child_add(NaElement("arg", "-timezone"))
args.child_add(NaElement("arg", "America/New_York"))
#   if module.params['date']:
# args.child_add(NaElement("arg", "-date"))
# args.child_add(NaElement("arg", ))

systemCli = NaElement("system-cli")
systemCli.child_add(args)
xo = s.invoke_elem(systemCli)

if(xo.results_errno() != 0):
    r = xo.results_reason()
    print (r)
    sys.exit (1)

print (xo.sprintf())
