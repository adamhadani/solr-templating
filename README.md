# solrnode-utils

### A set of utility scripts for templating solr configurations and working with multi-instance solr installations

solrnode-utils is a framework which encompasses a few Python and shell scripts that allow you to create templates of solr-backed search services,
package & deploy these templates, and use them to create any number of runnable instances on a production environment.

## Requirements

To use the framework, you will need the following:

* a Java Servlet container - Currently we support [Tomcat](http://tomcat.apache.org/index.html), however in the future this can be extended
  for other servers (e.g Jetty).
* [Solr](http://lucene.apache.org/solr/) - You will need to have the solr .WAR file available and visible to your servlet container

## Installation

To install the framework, use the included setup.py, e.g:

```bash
python setup.py install
```

This will by default install all the framework scripts into your global python environment, making
them available in your system PATH. 
You could also potentially install the framework under a Python [virtualenv](http://pypi.python.org/pypi/virtualenv).

## Connfiguration

There is a basic configuration that needs to exist before we can do anything.
The framework will look for the configuration file in /etc/solrnoderc and in ~/.solrnoderc.
An example for a minimal configuration file is provided under the examples/ dir. Once in place,
this will tell the framework where to find tomcat, solr.war and what are the base directories
that will hold all templates / instances created.

## Example Usage

Suppose you have 3 different solr-backed services which are part of your infrastructure, that need to each be
running standalone (e.g not as different cores under the same java servlet server).

* Create 3 template directory trees for these:

	```bash
	solrnode-create-tmpl -t people-search
	solrnode-create-tmpl -t item-search
	solrnode-create-tmpl -t backend-search 
	```

	After running these commands, you will end up with a directory per template type, containing a skeleton configuration
	that you can then tweak to your heart's desire.
	The resulting files are still not usable in themselves - you'll notice various properties in the .tmpl files use a template language markup (the excellent [Jinja2](http://jinja.pocoo.org/)) - Do not change these, as they are handled by the framework later on when instantiating templates.

	You can also drop in template-specific files (static configuration, JAR files, etc.) that should be bundled along as well.

	The resulting directory structure makes up your development tree - you can (and probably should) check it in your VCS.

	You can now create runnable instances based on your templates.
    For example, for the purposes of some logical sharding you might want to create multiple instances from a single service template, 
	and you can create these with different names and ports, e.g:

	```bash
	solrnode-create-inst -t people-search -i people-search-01 tomcat.port=8081 tomcat.shutdown_port=18081
	solrnode-create-inst -t people-search -i people-search-02 tomcat.port=8082 tomcat.shutdown_port=18082
	solrnode-create-inst -t item-search -i item-search-00 tomcat.port=8090 tomcat.shutdown_port=18090
	```

	To start or stop an instance, as well as get current status of a named instance, you can use the 
    solrnode-ctl. This command essentially provides the needed environment and wraps around a launcher.
    Currently, we support both 'plain' tomcat execution (delegating to the catalina.sh script), as well
    as using supervisord. For the latter, you will need to seperately configure your own supervisord.conf
    file and make sure supervisord daemon is running properly. So, for example, assuming you configured supervisord with
    the tomcat/solr service using the same names as you used for the instances, you would simply invoke solrnode-ctl thus:

	```bash
	solrnode-ctl --supervisord start people-search-01
	solrnode-ctl --supervisord status people-search-01
	solrnode-ctl --supervisord stop people-search-01
	```

	There is also a solrnode-ctl 'kill' command to brutally chop off any rogue instance that has not properly shut off earlier.
	This can happen as result of various resource freeing related issues, and involves clearing out any remaining PID/lock files etc.

## Packaging

A more realistic setting is one where you would be developing and testing templates and instances in one environment,
and then push out ready templates to your production environment, and instantiate them there.
The framework takes care of that aspect as well by introducing the notion of template packages. These allow you
to quickly tie up an arbitrary selection of local templates into a single distributable (.tar.gz file).
This file can then be installed on the target host using the solrnode-install-pkg command.
Notice that this means you would need solrnode-utils installed on both your development as well as production environments.

Example use case:

* Create a deployable package containing your templates. To create one, you simply pass all templates that should
be included (identified by their directory location in local file system). 
Assuming all previous templates are in current working dir:

	```bash
	solrnode-create-pkg *-search
	```

	This will result in a .tgz file containing all specified templates, stamped with the current timestamp and username by default.

* To deploy on remote machine (where solrnode-utils has also been installed):

	```bash
	solrnode-install-pkg <package_file.tgz>
	```

	Once deployed, the templates become globally available to the framework, and you can create any number of runnable instances based on them. 

## Documentation

Each script can be invoked with the -h flag to show detailed usage instructions.

## Development

If you'd like to contribute to / fork this project, bear in mind that for generating your own
source distributions you'd have to make sure setuptools (or distribute) picks up all the package
data files, specifically the default template we supply. Since setuptools by default uses VCS bindings
to identify tracked data files in order to decide which ones to include or not, you will want to have
the git setuptools package installed: [setuptools-git](http://pypi.python.org/pypi/setuptools-git)

## Credits

solrnode-utils was created by [Adam Ever-Hadani](http://github.com/adamhadani/)

## Contact

Adam Ever-Hadani

- http://github.com/adamhadani
- http://www.linkedin.com/in/adamhadani
- adamhadani@gmail.com

## License

solrnode-utils is available under the Apache license 2.0. See the LICENSE file for more info.
