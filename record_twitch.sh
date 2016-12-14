#!/bin/bash
for i in $(cat "/vagrant/usernames.txt"); do
  python3 "/vagrant/record.py" $i & >> log.txt
done
