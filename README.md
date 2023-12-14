# Tornado students application based on mongoDB

## Running MongoDB and Mongo-Express

This application relies on MongoDB, which can be run together with mongo-express using the docker-compose.yml file:
```bash
docker-compose up
```
The docker-compose.yaml file uses static ip addresses.
(this workaround has been required since there has been issues with tornado.testing using the port forwarding on the localhost) 

The MongoDB URI is hardcoded [here](https://github.com/michelescarlato/tornadomongo/blob/main/students_tornado.py#L13).
User and password are defined in the [docker-compose.yml](https://github.com/michelescarlato/tornadomongo/blob/main/docker-compose.yml#L12-L13) file.

In case you want to use a different IP schema, you can modify the IPAM configuration changing the [subnet](https://github.com/michelescarlato/tornadomongo/blob/main/docker-compose.yml#L8),
and modifying the [mongo ip address in the container](https://github.com/michelescarlato/tornadomongo/blob/main/docker-compose.yml#L22), as well as in the [mongo-express environment](https://github.com/michelescarlato/tornadomongo/blob/main/docker-compose.yml#L32),
and the [mongo-express ip address](https://github.com/michelescarlato/tornadomongo/blob/main/docker-compose.yml#L35).
 

To access **mongo-express**:
```
http://localhost:8000
```
After login with _admin/pass_ you will be able to manage the mongodb instance.


## Running the tornado_student python application

To isolate the environment, using Python3.10 as interpreter, I used a python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

To install the required dependencies:

```bash
pip3 -r requirements.txt
```

To run the _**students_tornado**_ application:
```bash
python3 students_tornado.py
```

## Operations

Populate the DB with one student, using the **_POST_** method and the json as a body:
```bash
curl -X "POST" "http://localhost:9000/" \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json; charset=utf-8' \
    -d $'{
        "name": "Lisa",
        "surname": "Kruger",
        "email": "lkruger@example.com"        
    }'
```

**GET** the student list, e.g., from the browser with:
```
http://localhost:9000/
```

or using curl:
```bash
curl -X "GET" "http://localhost:9000/"
```

or **GET** a specific student using its __id_:
```bash
curl -X "GET" "http://localhost:9000/657a73b5f39a9686a65944e6"
```

If you want to modify the student information, grab the __id_ from one of the previous output,
append it to the url, using the **PUT** method , e.g., in _curl_ and pass the new parameters as a json: 
```bash
curl -X "PUT" "http://localhost:9000/65797ca9bbdf7a1fb9b54022" \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json; charset=utf-8' \
    -d $'{        
        "name": "Lara",
        "surname": "Croft",
        "email": "lcroft@example.com"        
    }'
```

If you want to try the **_delete_** function, you can delete the created student, using the __id_ as a parameter in the next _DELETE_:
```bash
curl -X "DELETE" "http://localhost:9000/657a73d6f39a9686a65944e7"
```

Tests written with `tornado.tests` can be run from pycharm, but to be run from shell they should be on the same directory of students_tornado.py (because it is imported as a module).

**Postman** collection can be imported using Postman -> import -> [Collection URL](https://api.postman.com/collections/718114-14bde538-1ff7-4962-957c-4c96e59c99a4?access_key=PMAT-01HHJ3EDGRC30VTC9940XSN83W)

**Apache JMeter** .jmx file can be imported from File -> open -> [jmeter Thread Group.jmx](https://github.com/michelescarlato/tornadomongo/blob/main/tests/jmeter_Thread%20Group.jmx)



