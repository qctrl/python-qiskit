
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')


setup(
    long_description=readme,
    name='qctrl-qiskit',
    version='0.0.3',
    description='Q-CTRL Qiskit Adapter',
    python_requires='<3.9,>=3.7',
    project_urls={"repository": "https://github.com/qctrl/python-qiskit"},
    author='Q-CTRL',
    author_email='support@q-ctrl.com',
    license='Apache-2.0',
    keywords='quantum computing open source engineering qiskit',
    classifiers=['Development Status :: 5 - Production/Stable', 'Environment :: Console', 'Intended Audience :: Developers', 'Intended Audience :: Education', 'Intended Audience :: Science/Research', 'License :: OSI Approved :: Apache Software License', 'Natural Language :: English', 'Operating System :: OS Independent', 'Programming Language :: Python :: 3.6', 'Topic :: Scientific/Engineering :: Physics', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Embedded Systems', 'Topic :: System :: Distributed Computing'],
    packages=['qctrlqiskit'],
    package_dir={"": "."},
    package_data={},
    install_requires=['numpy==1.*,>=1.16.0', 'qctrl-open-controls==8.*,>=8.5.1', 'qiskit-ibmq-provider==0.*,>=0.3.3', 'qiskit-terra==0.*,>=0.12.0', 'scipy==1.*,>=1.3.0', 'toml==0.*,>=0.10.0'],
    extras_require={"dev": ["isort==5.*,>=5.7.0", "nbval==0.*,>=0.9.5", "pylama", "pylint", "pylint-runner", "pytest", "qctrl-visualizer==2.*,>=2.12.1", "sphinx==2.*,>=2.2.0"]},
)
