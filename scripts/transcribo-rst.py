#! python
try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description
from transcribo import rST, preferences
import os.path

# Get the file name of this script and search for a config file filename.yaml:
import sys
fn = sys.argv[0].replace('\\', '/')
fn = fn.split('/') [-1][:-3] # this cuts off the path, if any, and the .py suffix
fn = fn + 'yaml' # this is the config file name to be passed on to the preferences Config object
if os.path.exists(fn): preferences.add(fn)





publish_cmdline(writer = rST.Writer(), description = default_description)

