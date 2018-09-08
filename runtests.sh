#!/bin/sh

echo "testing with $(python2 -V 2>&1)"
python2 $(which nosetests) -v --with-coverage --cover-erase tests/

if test $? -eq 0 ; then
	echo

	echo "testing with $(python3 -V 2>&1)"
	python3 $(which nosetests) -v --with-coverage --cover-erase tests/
fi
