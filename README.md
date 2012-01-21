# solrnode-utils

### A set of utility scripts for templating solr configurations and working with multi-instance solr installations

solrnode-utils is a framework which encompasses a few Python and shell scripts that allow you to create templates of solr-backed search services,
package & deploy these templates, and use them to create any number of runnable instances on a production environment.

## Installation

To install the framework, use the included setup.py, e.g:
```bash
python setup.py install
```

This will by default install all the framework scripts into your global python environment, making
them available in your system PATH. 
You could also potentially install the framework under a Python [virtualenv](http://pypi.python.org/pypi/virtualenv).


## Example Usage

Suppose you have 3 different solr-backed services which are part of your infrastructure, that need to each be
running standalone (e.g not as different cores under the same java servlet server).

* You would create 3 template directory trees for these:

	```bash
	solrnode-create-tmpl -t people-search
	solrnode-create-tmpl -t item-search
	solrnode-create-tmpl -t backend-search 
	```

	After running these commands, you will end up with a directory per template type, containing a skeleton configuration
	that you can then tweak to your heart's desire.
	The resulting files are still not usable in themselves - you'll notice various properties in the .xml files use a template language markup
	to provide stubs for values that are injected by the framework later on, when creating instances from the template. (More on this below)

	You can also drop in template-specific solr plugins (JAR files) under the template's lib/ sub-directory.

	The resulting directory structure makes up your development tree - you can (and probably should) check it in your VCS.

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
	So for example, if for the purposes of some logical sharding you would need to create multiple instances from a single service template, 
	you could create these with different names and ports, e.g:

	```bash
	solrnode-create-inst -t people-search-01 -p 8081
	solrnode-create-inst -t people-search-02 -p 8082
	```

	To start or stop an instance, as well as get current status of a named instance, you can then use:

	```bash
	solrnode-ctl start people-search-01
	solrnode-ctl status people-search-01
	solrnode-ctl stop people-search-01
	```

	There is also a solrnode-ctl 'kill' command to brutally chop off any rogue instance that has not properly shut off earlier.
	This can happen as result of various resource freeing related issues, and involves clearing out any remaining PID/lock files etc.


## Documentation

Each script can be invoked with the -h flag to show detailed usage instructions.

## Credits

solrnode-utils was created by [Adam Ever-Hadani](http://github.com/adamhadani/)

## Contact

Adam Ever-Hadani

- http://github.com/adamhadani
- http://www.linkedin.com/in/adamhadani
- adamhadani@gmail.com

## License

solrnode-utils is available under the Apache license 2.0. See the LICENSE file for more info.
