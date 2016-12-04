#!/bin/sh

test=$(which nosetests)

echo "testing with $(python2 -V 2>&1)"
python2 $test --rednose -v tests/

if [ $? == 0 ]; then
	echo

	echo "testing with $(python3 -V 2>&1)"
	python3 $test --rednose -v tests/
fi
