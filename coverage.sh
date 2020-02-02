#!/bin/bash

coverage run -m unittest discover -v
coverage run report
