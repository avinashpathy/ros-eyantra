#!/bin/bash

# Store URL in a variable
URL1="http://www.hivemq.com/demos/websocket-client/"
                                            
URL2="https://script.google.com/macros/s/AKfycbzrUFi_nOO-9pNE88PNcOKtl2z9ki35SFWFv3dHPlNsVyUe0UxP/exec"  #  need to change url 
# Print some message
echo "** Opening $URL1 in Firefox **"

# Use firefox to open the URL in a new window
firefox -new-window $URL1 
firefox -new-window $URL2
