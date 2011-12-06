__doc__ = """
A Django template loader for loading and converting SHPAML markup to HTML

The django SHPAML template loader uses the official Python SHPAML implementation
which can be found at http://shpaml.webfactional.com/

Note: the SHPAML implementation from the above link is included for your
convenience.
"""

from setuptools import setup

setup(
    name='django-shpaml',
    version='1.0.2',
    author='James Robert',
    description=('A Django template loader for loading and converting '
                 'SHPAML markup to HTML'),
    license='BSD',
    keywords='django shpaml',
    url='http://shpaml.com',
    packages=['shpaml'],
    long_description=__doc__,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ]
)
