
try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description

from transcribo import docutils_txt_writer

publish_cmdline(writer = docutils_txt_writer.Writer(), description = default_description)

