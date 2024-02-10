# efaLive project
This project contains the efaLive Debian package and most of the files and scripts that form the glue between the Debian system and the efa software in an efaLive system.

efaLive is a live CD (or RaspberryPi image) that runs the rowing and canoeing log book software [efa](http://efa.nmichael.de/) on a Linux system in a so called KIOSK mode. This means that the system, where efaLive is started on, will directly boot into the efa software. So a user in front of the system can use the efa software only. There is no direct access to other software.

## Binaries and documentation
For more information about efaLive, have a look to the efaLive documentation on [my homepage](https://www.hannay.de/en/efalive/). There you can also find efaLive CD images for download.

## Related projects
* [Debian GNU/Linux project](http://www.debian.org/)
* [efaLive Docker](https://github.com/kayhannay/efalive_docker) - the Docker file to create an efaLive development environment
* [efaLive CD](https://github.com/kayhannay/efalive_cd) - the live CD build configuration
* [efaLive PI](https://github.com/kayhannay/efalive_pi) - efaLive image for Raspberry Pi
* [efaLive](https://github.com/kayhannay/efalive) - the glue code between Debian and the efa software (this project)
* [efa 2](https://github.com/kayhannay/efa2) - the Debian package configuration of the efa software
* [efa](http://efa.nmichael.de/) - the rowing and canoeing log book software

##Requirements
The efaLive project consists mainly of Bash shell scripts, a small Python GUI for administratrive tasks and a Python daemon. To run the efaLive-Setup and daemon tool, you at least need the following packages:

* Python 3
* [Poetry](https://python-poetry.org/)

To build the Debian package, you need to have [dpkg-dev](http://packages.debian.org/bookworm/dpkg-dev) installed.

## How to build
To build the debian package, there is a script for convenience:

```shell
build_deb.sh
```

## Run efaLive setup and daemon
Change to the efalive project directory. There you can run efaLive setup by executing

Only once to set up the virtual environment:
```shell
poetry install
```

```shell
poetry run python efalivesetup.py ./tmp
```


This will start the efaLive setup tool and use ./tmp for the settings.

efaLive daemon can be started by

```shell
poetry run python efalivedaemon.py ~/.efalive start
```

The log file will be written to the current directory.

## Run the tests
To run the tests execute

```shell
poetry run pytest
```
