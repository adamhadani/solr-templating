#!/usr/bin/env python
"""
solrnode utilities for working with environment variables and settings
"""

import os
import sys
from configparser import SafeConfigParser

home = sys.env('HOME')
rc_locations = [
    '/etc/solrnoderc',
    '{0}/.solrnoderc'.format(home)
]

