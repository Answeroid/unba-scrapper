#!/bin/bash

while true; do
  read -r -p "Please provide spider name: " name
  if [[ -n "$name" ]] ; then
    # Check if the spider exists
    if scrapy list | grep -q "$name"; then
      # Spider exists, run it
      scrapy crawl "$name" -O res/"$name".csv -O res/"$name".json | tee res/crawl.log
      break
    else
      echo "Error: Spider '$name' not found. Please enter a valid spider name."
    fi
  else
    echo "Error: Please enter a valid spider name."
  fi
done
