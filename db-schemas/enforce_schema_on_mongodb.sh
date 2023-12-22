## to connect from localhost to the docker container (with port forwarded)
# mongosh mongodb://root:example@localhost:27017/

## to switch db
# use university

# university>
db.createCollection("students")
db.runCommand({
    "collMod": "students",
    "validator": {
        $jsonSchema: {
            "bsonType": "object",
            "description": "Document describing a mountain peak",
            "required": ["_id", "name", "surname", "email"],
            "properties": {
                "_id": { "bsonType": "objectId" },
                "name": { "bsonType": "string" },
                "surname": { "bsonType": "string" },
                "email": { "bsonType": "string" },
                "nationality" : { "bsonType": "string" },
                "possible_nationality" : { "bsonType": "string", "description": "Retrieved querying an external API" }
              },
        }
    }
})


# db.students.drop() --> to drop the collection