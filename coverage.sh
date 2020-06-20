#!/bin/bash

coverage run --source=. -m pytest tests -v
coverage report -m 
