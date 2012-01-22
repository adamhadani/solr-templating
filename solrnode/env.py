#!/usr/bin/env python
"""
solrnode utilities for working with environment variables and settings
"""

import os
import sys
import operator
from itertools import imap
from ConfigParser import SafeConfigParser

_home = os.environ['HOME']
_rc_locations = [
    '/etc/solrnoderc',
    '{0}/.solrnoderc'.format(_home)
]

class SolrNodeEnv(dict):
    """Encapsulates the environment
    as used by the framework. This is typified
    by a nested dict-like data structure which
    can have settings interleaved from config files
    as well as used-supplied CLI arguments"""
    
    def __init__(self):
        super(dict, self).__init__()
        
        self.update_conf_files(_rc_locations)
        
    def update_conf_files(self, filenames):
        """Update environment from a sequence of
        configuration file locations. These are expected
        to be in the simple INI-like format readable
        by Python's configparser"""
        config = SafeConfigParser()
        num_read = config.read(filenames)    
        if not num_read:
            self.LOG.warning("Could not find solrnoderc configuration file in any of the locations searched (%s)",
                             filenames)
            return
        
        for section in config.sections():
            self.setdefault(section, {})
            self[section].update(dict(config.items(section)))
            
    def update_user_args(self, user_args):
        """Update environment from a sequence
        of user arguments. These are expected to be of the
        form <var_name>=<var_value>, and can contain
        dotted notation (e.g 'fs.path=/my/path')"""
        
        for (key, value) in imap(lambda x: x.split("="), user_args):
            split_key = key.split(".")
            curr_node = self
            for ns in split_key[:-1]:
                curr_node.setdefault(ns, {})
                curr_node = curr_node[ns]
            curr_node[split_key[-1]] = value

class TemplateManifest(object):
    """A Template manifest is a bundle
    of definitions that gives the framework
    reflection-like access to the template.
    This is used esp. when rendering an instance
    from a import template, e.g to keep track of
    required variable definitions"""
    
    def __init__(self, metadata, required_vars=None):
        self.metadata = metadata
        self.required_vars = required_vars or []
        
    def __unicode__(self):
        return u"\n".join([
            "Template name: {0}".format(self.metadata['name']),
            "Author: {0}".format(self.metadata['author']),
            "Created on: {0}".format(self.metadata['created_on']),
            
            "Required vars:\n{0}".format("  " + \
                "\n  ".join(self.required_vars))
            ])
    __repr__ = __unicode__
    
    @classmethod
    def from_file(cls, filename):
        config = SafeConfigParser()
        config.read(filename)
        
        metadata = dict(config.items('metadata'))
        
        required_vars = map(operator.itemgetter(1),
                config.items('required_vars'))
        
        return TemplateManifest(metadata=metadata, 
                required_vars=required_vars)
            