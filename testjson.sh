#!/bin/sh
find themes/ -name "*.json"|grep -v invalid|
while read f; do
  cat "$f" | json_verify 2>&1 > /dev/null | sed "1 s@\(.*error\)@\nError in $f\n\1@g"
done
