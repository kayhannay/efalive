#!/bin/bash

pipenv --rm
pipenv install -d
pipenv run nosetests --with-coverage --cover-inclusive --cover-erase --cover-package=. -w efalive
pipenv --rm

exit $?
