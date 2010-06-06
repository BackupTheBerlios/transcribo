
import sys, shutil, os
from distutils.core import setup, Extension




longdescr = open('README.txt').read()


arg_dict = dict(
    name = "Transcribo", version = "0.7",
    author = "Dr. Leo",
    author_email = "dr-leo@berlios.de",
    url = "http://transcribo.berlios.de",
    description = "A general purpose plain text renderer for arbitrary input formats including frontends for reStructuredText and plain text",
    long_description = longdescr,
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
         'Development Status :: 3 - Alpha',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
                'Topic :: Text Processing',
                'Topic :: Adaptive Technologies',
                'Topic :: Printing',
    ],
    packages = ['transcribo', 'transcribo.renderer'],
    package_data = {'transcribo' : ['config.yaml'],
        'transcribo.renderer' : ['styles/' + fn for fn in os.listdir('transcribo/renderer/styles/')]},
        py_modules = ['yaconfig'],
    scripts = ['scripts/transcribo-txt.py', 'scripts/transcribo-rst.py'],
        requires = ['docutils', 'PyYAML'],
        provides = ['transcribo']
)



setup(**arg_dict)

