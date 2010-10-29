
import sys, shutil, os
from distutils.core import setup, Extension




longdescr = open('README.txt').read()

all_cfg_files = ['config.yaml']
all_cfg_files.extend(['styles/' + fn
    for fn in os.listdir('transcribo/styles/')])

arg_dict = dict(
    name = "Transcribo", version = "0.7.1",
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
    package_data = {'transcribo' : all_cfg_files},
    scripts = ['scripts/transcribe.py'],
        requires = ['docutils', 'PyYAML', 'argparse'],
        provides = ['transcribo']
)



setup(**arg_dict)

