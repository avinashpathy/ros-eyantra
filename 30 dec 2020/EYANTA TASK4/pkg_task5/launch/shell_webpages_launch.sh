#!/bin/bash     
URL1="https://docs.google.com/spreadsheets/d/1lStRXt0zWrFtgl89LziSmylPpJe-DfPQ4bPfMFeRvgk/edit#gid=0"
# Print some message
echo "** Opening 
     $URL1 in Firefox **"

# Use firefox to open the URL in a new window
firefox -new-window $URL1 

