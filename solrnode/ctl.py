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
"""Control mecahnics for node types"""

import os
import subprocess

class SolrNodeCtl(object):
    """Encapsulate environment
    and logic for controlling service
    runtime"""
    
    def __init__(self, **opts):
        self.opts = opts
        
        self.setenv()
        
    def setenv(self):
        """Create the appropriate (OS) environment
        for executing service"""
        
        os.environ['CATALINA_BASE'] = os.path.join(
            self.opts['instances_base_dir'], self.opts['instance_name'], 
            'catalina-base')
        os.environ['CATALINA_PID'] = os.path.join(
            os.environ['CATALINA_BASE'], 'catalina.pid')
        os.environ['CATALINA_OPTS'] = self.opts['catalina_opts']
    
    def start(self):
        """Start service"""
        return subprocess.call([
                os.path.join(self.opts['catalina_home'], 
                            'bin', 'catalina.sh'),
                "start"
                ])
        
    def stop(self):
        """Stop service"""
        return subprocess.call([
                os.path.join(self.opts['catalina_home'], 
                             'bin', 'catalina.sh'),
                "stop"
                ])
        
    def status(self):
        """Probe service status"""
        return subprocess.call([
                os.path.join(self.opts['catalina_home'], 
                             'bin', 'catalina.sh'),
                "status"
                ])
        
    def kill(self):
        """Kill service (kill -9)"""
        return subprocess.call([
                os.path.join(self.opts['catalina_home'], 
                             'bin', 'catalina.sh'),
                "stop",
                "-force"
                ])
        
    