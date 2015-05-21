#efaLive project
This project holds the content of the efaLive Debian package and contains most of the files and scripts that form the glue between the Debian system and the efa software in an efaLive system.

efaLive is a live CD that runs the rowing and canoeing log book software [efa](http://efa.nmichael.de/) on a Linux system in a so called KIOSK mode. This means that the system, where efaLive is started on, will directly boot into the efa software. So a user in front of the system can use the efa software only. There is no direct access to other software.

##Binaries and documentation
For more information about efaLive, have a look to the efaLive documentation on [my homepage](http://www.hannay.de/index.php/efalive/). There you can also find efaLive CD images for download.

##Related projects
* [Debian GNU/Linux project](http://www.debian.org/)
* [efaLive Docker](https://github.com/efalive/efalive_docker) - the Docker file to create an efaLive development environment
* [efaLive CD](https://github.com/efalive/efalive_cd) - the live CD build configuration
* [efaLive](https://github.com/efalive/efalive) - the glue code between Debian and the efa software (this project)
* [efa 2](https://github.com/efalive/efa2) - the Debian package configuration of the efa software
* [efa](http://efa.nmichael.de/) - the rowing and canoeing log book software

##Requirements
The efaLive project consists mainly of Bash shell scripts, a small Python GUI for administratrive tasks and a Python daemon. To run the efaLive-Setup and daemon tool, you at least need the following packages:

* [python-gtk2](http://packages.debian.org/jessie/dpkg-dev)
* [arandr](http://packages.debian.org/jessie/arandr)
* [python-gudev](http://packages.debian.org/jessie/python-gudev)
* [python-pam](http://packages.debian.org/jessie/python-pam)
* [python-daemon](http://packages.debian.org/jessie/python-daemon)
* [python-pyudev](http://packages.debian.org/jessie/python-pyudev)
* [python-mock](http://packages.debian.org/jessie/python-mock)

To build the Debian package, you need to have [dpkg-dev](http://packages.debian.org/jessie/dpkg-dev) installed.

##How to build
To build the debian package, there is a script for convenience:

```shell
build_deb.sh
```

##Run efaLive setup and daemon
There are two scripts to start the efaLive setup or the efaLive dameon tool. Change to the src/python directory. There you can run efaLive setup by executing

```shell
./efalive-setup ./tmp
```

This will start the efaLive setup tool and use ./tmp for the settings.

efaLive daemon can be started by

```shell
./efalive-daemon
```

The log file will be written to the current directory.

##Run the tests
To run the tests, change to the /src/python directory and execute

```shell
./run_tests.sh
```
