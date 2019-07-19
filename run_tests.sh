#!/bin/bash

pipenv run nosetests --with-coverage --cover-inclusive --cover-erase --cover-package=. -w efalive

exit $?
