#!/bin/bash

# Store URL in a variable
URL1="http://www.hivemq.com/demos/websocket-client/"
     
URL2="https://docs.google.com/spreadsheets/d/1gI83z-xyDCNz5ZD4jdCh2m1ZNOTk2Zv4kqUjiiDxZg8/edit#gid=0"
# Print some message
echo "** Opening $URL1  
     $URL2 in Firefox **"

# Use firefox to open the URL in a new window
firefox -new-window $URL1 $URL2

