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
from abc import abstractmethod, ABCMeta

class NodeCtl(object):
    """Base class for defining
    a control proxy"""
    
    __metaclass__ = ABCMeta
    
    def __init__(self, **opts):
        self.opts = opts
        
    @abstractmethod
    def setenv(self):
        """Set any (OS) environment variables
        that need to be set before invoking"""
        
    @abstractmethod
    def start(self):
        pass
        
    @abstractmethod
    def stop(self):
        pass
        
    @abstractmethod
    def status(self):
        pass
        
    @abstractmethod
    def kill(self):
        pass
        
class SupervisordNodeCtl(NodeCtl):
    """Encapsulate environment and logic for
    controlling service using supervisord"""
    
    def __init__(self, **opts):
        super(SupervisordNodeCtl, self).__init__(**opts)
        
    def setenv(self):
        os.environ['CATALINA_BASE'] = os.path.join(
            self.opts['instances_base_dir'], self.opts['instance_name'], 
            'catalina-base')
        os.environ['CATALINA_PID'] = os.path.join(
            os.environ['CATALINA_BASE'], 'catalina.pid')
        os.environ['CATALINA_OPTS'] = self.opts['catalina_opts']
    
    def start(self):
        return self.supervisorctl('start')
    
    def stop(self):
        return self.supervisorctl('stop')
        
    def status(self):
        return self.supervisorctl('status')
        
    def kill(self):
        return self.supervisorctl('kill')
        
    def supervisorctl(self, cmd):
        return subprocess.call([
            "supervisorctl", 
            cmd,
            self.opts['instance_name']
            ])
        
        
class TomcatNodeCtl(NodeCtl):
    """Encapsulate environment and logic for controlling 
    tomcat service runtime"""
    
    def __init__(self, **opts):
        super(SupervisordNodeCtl, self).__init__(**opts)
        
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
        
    