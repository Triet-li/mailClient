#!/bin/bash

file="config.json"
smtpPort=`jq -r '.SMTP' "$file"`
pop3Port=`jq -r '.POP3' "$file"`

java -jar test-mail-server-1.0.jar -s $smtpPort -p $pop3Port -m ./
