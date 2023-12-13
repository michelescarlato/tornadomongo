# Tornado students application based on mongoDB

This application relies on MongoDB, which can be run together with mongo-express using the docker-compose.yml file:

```bash
docker-compose up
```

To isolate the environment, using Python3.10 as interpreter, I used a python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

To install the required dependencies:

```bash
pip3 -r requirements.txt
```

Despite mongo is accessible also from the localhost, I used the container IP address to connect to mongo.
Switching to localhost I had issues running the tests written with `tornado.testing`. 
To retrieve the container ip:
```bash
docker inspect   -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $MONGODB_CONTAINER_NAME
```

MongoDB URI is hardcoded [here](https://github.com/michelescarlato/tornadomongo/blob/main/students_tornado.py#L13).
User and password are defined in the [docker-compose.yml](https://github.com/michelescarlato/tornadomongo/blob/main/docker-compose.yml#L12-L13) file.

To access **mongo-express**:
```
http://localhost:8000
```
Login with _admin/pass_.


To run the _**students_tornado**_ application:
```bash
python3 students_tornado.py
```

Populate the DB with one student:
```bash
curl -X "POST" "http://localhost:9000/" \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json; charset=utf-8' \
    -d $'{
        "name": "Jane",
        "surname": "Doe",
        "email": "jdoe@example.com"        
    }'
```

Get the student list, e.g., from the browser with:
```
http://localhost:9000/
```

If you want to modify the Student information, grab the __id_ from the browser's output and append it to the url, using the PUT method , e.g., in _curl_: 
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

If you want to try the **_delete_** function, you can delete the created student, using the "_id" as a parameter in the next _DELETE_:
```bash
curl -X "DELETE" "http://localhost:9000/65797ca9bbdf7a1fb9b54022"
```


Tests written with `tornado.tests` can be run from pycharm, but to be run from shell they should be on the same directory of students_tornado.py (because it is imported as a module).

**Postman** collection can be imported using Postman -> import -> [Collection URL](https://api.postman.com/collections/718114-14bde538-1ff7-4962-957c-4c96e59c99a4?access_key=PMAT-01HHJ3EDGRC30VTC9940XSN83W)

**Apache JMeter** .jmx file can be imported from File -> open -> [jmeter Thread Group.jmx](https://github.com/michelescarlato/tornadomongo/blob/main/tests/jmeter_Thread%20Group.jmx)



