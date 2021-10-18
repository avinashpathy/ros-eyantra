import requests


tm = 100;
# defining our sheet name in the 'id' variable and the the column where we want to update the value
parameters = {"id":"Sheet1", "Order ID":"1000","Priority":"HP","Time Taken":"487","Longitude":"12.97","Latitude":"77.59"} 
URL = "https://script.google.com/macros/s/AKfycbx4_KSB3dGiZOL_ExE1DJ_x1RrLXo2-onAlmf9jL6Ksmshvnuael-y6mw/exec"
response = requests.get(URL, params=parameters,timeout=tm)


parameters = {"id":"Sheet1", "Order ID":"1001","Priority":"HP","Time Taken":"356","Longitude":"12.29","Latitude":"76.63"} 
URL = "https://script.google.com/macros/s/AKfycbx4_KSB3dGiZOL_ExE1DJ_x1RrLXo2-onAlmf9jL6Ksmshvnuael-y6mw/exec"
response = requests.get(URL, params=parameters,timeout=tm)

parameters = {"id":"Sheet1", "Order ID":"1002","Priority":"HP","Time Taken":"247","Longitude":"28.7041","Latitude": "77.1025"} 
URL = "https://script.google.com/macros/s/AKfycbx4_KSB3dGiZOL_ExE1DJ_x1RrLXo2-onAlmf9jL6Ksmshvnuael-y6mw/exec"
response = requests.get(URL, params=parameters,timeout=tm)

parameters = {"id":"Sheet1", "Order ID":"1003","Priority":"HP","Time Taken":"138","Longitude":"19.0760","Latitude": "72.8777"} 
URL = "https://script.google.com/macros/s/AKfycbx4_KSB3dGiZOL_ExE1DJ_x1RrLXo2-onAlmf9jL6Ksmshvnuael-y6mw/exec"
response = requests.get(URL, params=parameters,timeout=tm)


parameters = {"id":"Sheet1", "Order ID":"1004","Priority":"HP","Time Taken":"97","Longitude":"17.3850","Latitude": "78.4867"} 
URL = "https://script.google.com/macros/s/AKfycbx4_KSB3dGiZOL_ExE1DJ_x1RrLXo2-onAlmf9jL6Ksmshvnuael-y6mw/exec"
response = requests.get(URL, params=parameters,timeout=tm)



