__doc__ = """
A Django template loader for loading and converting SHPAML markup to HTML

Note: A SHPAML implementation is included for your
convenience. If you are interested in using shpaml alone, please see
shpaml/shpaml.py
"""

from setuptools import setup

setup(
    name='django-shpaml',
    version='1.1.0',
    author='James Robert',
    description=('A Django template loader for loading and converting '
                 'SHPAML markup to HTML'),
    license='BSD',
    keywords='django shpaml',
    url='http://shpaml.com',
    install_requires=[
        "django >= 1.2",
    ],
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
