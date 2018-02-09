#!/usr/bin/env python3

import os.path
from imp import load_source
from setuptools import setup


version = load_source('version', os.path.abspath('libinput/version.py'))


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as fd:
	long_description = fd.read()


classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Developers',
	'License :: OSI Approved :: MIT License',
	'Operating System :: POSIX :: Linux',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Topic :: Software Development :: Libraries']


setup(
	name='python-libinput',
	version=version.__version__,
	description='Object-oriented wrapper for libinput using ctypes',
	long_description=long_description,
	url='https://github.com/OzymandiasTheGreat/python-libinput',
	author='Tomas Ravinskas',
	author_email='tomas.rav@gmail.com',
	license='MIT',
	classifiers=classifiers,
	packages=['libinput'],
	package_dir={'libinput': 'libinput'},
	install_requires=[
		'aenum;python_version<"3.6"',
		'selectors34;python_version<"3.4"',
		'monotonic;python_version<"3.3"'])
