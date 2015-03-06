__doc__ = """
A Django template loader for loading and converting SHPAML markup to HTML

Note: A SHPAML implementation is included for your
convenience. If you are interested in using shpaml alone, please see
shpaml/shpaml.py
"""

from setuptools import setup

setup(
    name='django-shpaml',
    version='1.3.0',
    author='James Robert',
    author_email='shpaml@jiaaro.com',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ]
)
