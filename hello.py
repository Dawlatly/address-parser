#!/opt/conda/bin/python3.6

import cgi, cgitb
import json
from run import parseAddress
form = cgi.FieldStorage() 
address = parseAddress(str(form.getvalue('address')))

with open('data.json', 'w+') as outfile:  
    json.dump(address, outfile)

print ("Content-type:text/html\r\n\r\n")

print ("<html>")
print ("<head><title>Hello</title></head>")
print ("<body>")
print ("<p>It worksssss</p>")
print (address)
print ("</body>")
print ("</html>")