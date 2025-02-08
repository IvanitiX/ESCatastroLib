from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.1rc0'
DESCRIPTION = 'Description'
PACKAGE_NAME = 'ESCatastroLib'
AUTHOR = 'Iván V.R'
EMAIL = 'IvanVR@protonmail.com'
GITHUB_URL = 'github.com/IvanitiX/ESCatastroLib'

setup(
    name = PACKAGE_NAME,
    packages=find_packages(include=['ESCatastroLib', 'ESCatastroLib.*']),
    version = VERSION,
    license='Apache License, Version 2.0',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = [],
    install_requires=[ 
        'requests',
        'xml2dict'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3',
    ],
)
