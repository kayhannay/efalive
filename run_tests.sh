#!/bin/bash

pipenv --rm
pipenv install -d
pipenv run nosetests --with-coverage --cover-inclusive --cover-erase --cover-package=. -w efalive
RESULT=$?
echo "Result: $RESULT"
pipenv --rm

exit $RESULT

