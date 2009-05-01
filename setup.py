
import sys, shutil
from distutils.core import setup, Extension




longdescr = """Transcribo is a renderer backend for plain text output.\
  
It ships with a frontend that is a writer component for docutils.\

Note that Transcribo is in alpha status. It is published under the GPL 3.0.

Contact the author at fhaxbox66@googlemail.com.d


"""

arg_dict = dict(
    name = "Transcribo", version = "0.1",
    author = "Dr. Leo",
    author_email = "fhaxbox66@googlemail.com",
    url = "http://developer.berlios.de/projects/transcribo/",
    description = "An extensible plain text renderer for arbitrary input sources and content formats including a frontend for reStructuredText",
    long_description = longdescr,
    classifiers = [
        'Intended Audience :: Developers',
         'Development Status :: 3 - Alpha',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
                'Topic :: Text Processing',
    ],
    packages = ['transcribo', 'transcribo.renderer']
)



setup(**arg_dict)

