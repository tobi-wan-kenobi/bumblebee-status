#!/bin/sh

test=$(which nosetests)

echo "testing $(python2 -V 2>&1)"
python2 $test --rednose -v tests/

echo

echo "testing $(python3 -V 2>&1)"
python3 $test --rednose -v tests/
