#!/bin/sh

test=$(which nosetests)
python2 $test --rednose -v tests/
python3 $test --rednose -v tests/
