#!/bin/sh

find themes/ -name "*.json"|xargs cat|json_verify -s
