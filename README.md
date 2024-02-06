Make sure that Docker and docker-compose is installed 

docker build -t app .

docker run --name my_app -d -p 5000:5000 app

# HomeTask

## APP

### Dependencies

1. Latest version of docker installed
2. Latest version of docker-compose installed

### Installing

* Build container with an application with:
 ```docker build -t app .```
* App can be run with: 
``` docker run --name my_app -d -p 5000:5000 app```
* Yu can access the server via http://localhost:5000

### Executing program

* App can be run with: 
``` docker run --name my_app -d -p 5000:5000 app```
* Application can be accessed the via http://localhost:5000

## Test

### Installing

* Install requirements.txt from test/ using pip install
``` pip install -r requirements.txt```

### Execute
 
* Test cases and expected results are in test/test_app.py
* Execute 
``` pytest ```
while in test/ to run the tests 

### Results
* Logs can be found in test/logs
* Test report: test/report.xml

