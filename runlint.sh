#!/bin/sh

find . -name "*.py"|xargs pylint
