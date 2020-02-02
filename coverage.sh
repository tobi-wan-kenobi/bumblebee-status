#!/bin/bash

coverage run -m unittest discover -v -b
coverage report -m 
