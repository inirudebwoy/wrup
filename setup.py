#  -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    name='wrup',
    version="0.0.1",
    description='Upload posts to wordpress',
    long_description=open('README.rst').read(),
    license='GPLv2',
    author='Michal Klich',
    author_email='michal@michalklich.com',
    include_package_data=False,
    # packages=['wrup'],
    url='https://github.com/inirudebwoy/wrup',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
