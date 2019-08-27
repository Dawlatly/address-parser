# address-parser
This is an small cgi script that makes use of Conditional Random Fields to parse Malaysian addresses that are given into seperate components.

## To train the data:

* In run.py, uncomment the block of code (#Training the data begins here... Until Here)
* Execute run.py

## To run the address parser:

* Run command `docker build -t`
* Run command `docker run -it -p 9090:80 --name address-parser address-parser`
* Run in linux command `service apache2 start`
* In the web browser go to ip:80/cgi-bin/hello.py?address=InsertAddress
