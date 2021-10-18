import requests


tm = 100;
# defining our sheet name in the 'id' variable and the the column where we want to update the value
parameters = {"id":"Sheet1", "Order":"1000","Time Taken":"487","X Coordinate":"12.9716","Y Coordinate": "77.5946"} 
URL = "https://script.google.com/macros/s/AKfycbxzaLdibFoeWphDGcIl7WiJXXbcX-J_WwqLJMnpCXpXeQkaqPThc5zb3g/exec"
response = requests.get(URL, params=parameters,timeout=tm)


parameters = {"id":"Sheet1", "Order":"1001","Time Taken":"356","X Coordinate":"12.2958","Y Coordinate": "76.6394"} 
URL = "https://script.google.com/macros/s/AKfycbxzaLdibFoeWphDGcIl7WiJXXbcX-J_WwqLJMnpCXpXeQkaqPThc5zb3g/exec"
response = requests.get(URL, params=parameters,timeout=tm)

parameters = {"id":"Sheet1", "Order":"1002","Time Taken":"247","X Coordinate":"28.7041","Y Coordinate": "77.1025"} 
URL = "https://script.google.com/macros/s/AKfycbxzaLdibFoeWphDGcIl7WiJXXbcX-J_WwqLJMnpCXpXeQkaqPThc5zb3g/exec"
response = requests.get(URL, params=parameters,timeout=tm)

parameters = {"id":"Sheet1", "Order":"1003","Time Taken":"138","X Coordinate":"19.0760","Y Coordinate": "72.8777"} 
URL = "https://script.google.com/macros/s/AKfycbxzaLdibFoeWphDGcIl7WiJXXbcX-J_WwqLJMnpCXpXeQkaqPThc5zb3g/exec"
response = requests.get(URL, params=parameters,timeout=tm)


parameters = {"id":"Sheet1", "Order":"1004","Time Taken":"97","X Coordinate":"17.3850","Y Coordinate": "78.4867"} 
URL = "https://script.google.com/macros/s/AKfycbxzaLdibFoeWphDGcIl7WiJXXbcX-J_WwqLJMnpCXpXeQkaqPThc5zb3g/exec"
response = requests.get(URL, params=parameters,timeout=tm)

parameters = {"id":"Sheet1", "Order":"1005","Time Taken":"109","X Coordinate":"34.0837","Y Coordinate": "74.7973"} 
URL = "https://script.google.com/macros/s/AKfycbxzaLdibFoeWphDGcIl7WiJXXbcX-J_WwqLJMnpCXpXeQkaqPThc5zb3g/exec"
response = requests.get(URL, params=parameters,timeout=tm)

parameters = {"id":"Sheet1", "Order":"1006","Time Taken":"219","X Coordinate":"13.3379","Y Coordinate": "77.1173"} 
URL = "https://script.google.com/macros/s/AKfycbxzaLdibFoeWphDGcIl7WiJXXbcX-J_WwqLJMnpCXpXeQkaqPThc5zb3g/exec"
response = requests.get(URL, params=parameters,timeout=tm)

parameters = {"id":"Sheet1", "Order":"1007","Time Taken":"49","X Coordinate":"26.1445","Y Coordinate": "91.7362"} 
URL = "https://script.google.com/macros/s/AKfycbxzaLdibFoeWphDGcIl7WiJXXbcX-J_WwqLJMnpCXpXeQkaqPThc5zb3g/exec"
response = requests.get(URL, params=parameters,timeout=tm)

parameters = {"id":"Sheet1", "Order":"1008","Time Taken":"783","X Coordinate":"22.7196","Y Coordinate": "75.8577"} 
URL = "https://script.google.com/macros/s/AKfycbxzaLdibFoeWphDGcIl7WiJXXbcX-J_WwqLJMnpCXpXeQkaqPThc5zb3g/exec"
response = requests.get(URL, params=parameters,timeout=tm)


