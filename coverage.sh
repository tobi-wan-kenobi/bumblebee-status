#!/bin/bash

coverage run --source=. -m unittest discover -v -b
coverage report -m 
