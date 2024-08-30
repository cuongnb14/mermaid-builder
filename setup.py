import os
from setuptools import find_packages, setup

VERSION = '1.0.1'
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mermaid-builder',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Build mermaid by python code',
    long_description=README,
    url='https://github.com/cuongnb14/mermaid-builder',
    author='Cuong Nguyen',
    author_email='cuongnb14@gmail.com',
    classifiers=[
        'Environment :: Mermaid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[],
)
