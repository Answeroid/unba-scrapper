#!/bin/bash

while true; do
  read -r -p "\nPlease provide spider name: " name
  if [[ -n "$name" ]] ; then
    scrapy crawl "$name" -O res/"$name".csv -O res/"$name".json
  else
    echo "Please respond correctly."
  fi
done