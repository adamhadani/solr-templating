#!/usr/bin/env python
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#  
#      http://www.apache.org/licenses/LICENSE-2.0 
#     
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
import glob

from setuptools import setup, find_packages

SCRIPT_FILES = glob.glob('scripts/*')

setup(  
    name         = 'solr-templating',
    version      = '0.1',
    description  = 'Solr-backed search service templating and control framework',
    author       = 'Adam Ever-Hadani',
    author_email = 'adamhadani@gmail.com',
    url          = 'http://github.com/adamhadani/solr-templating',
    keywords     = ['solr', 'search' ],

    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",        
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators"        
        ],
    long_description = """\
For detailed description, see the project GitHub page.

This software is distributed under the Apache 2.0 license.
""",
    
    install_requires = [
        "jinja2>=2.6"
    ],

    packages = find_packages(),
    namespace_packages = ['solrnode'],

    scripts = SCRIPT_FILES,

    include_package_data = True,
)

