
try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description

from transcribo import rST

publish_cmdline(writer = rST.Writer(), description = default_description)

