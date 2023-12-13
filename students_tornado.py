import asyncio
import tornado.ioloop
import tornado.web
import tornado.escape
import motor.motor_asyncio
import motor.motor_tornado
from tornado.httpclient import AsyncHTTPClient
from bson import ObjectId, json_util
import json
import configparser
from operator import itemgetter

uri = 'mongodb://root:example@172.20.0.2:27017/'
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.university


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    async def get(self, student_id=None):
        if student_id is not None:
            if (student := await self.settings["db"]["students"].find_one({"_id": student_id})) is not None:
                return self.write(student)
            else:
                raise tornado.web.HTTPError(404)
        else:
            students = await self.settings["db"]["students"].find().to_list(1000)
            self.set_status(200)
            return self.write(json_util.dumps({"students": students}))

    async def post(self):
        student = tornado.escape.json_decode(self.request.body)
        student["_id"] = str(ObjectId())
        print(f"Adding student with id: {str(student['_id'])}")
        url = f'https://api.nationalize.io/?name={student["name"]}'
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url)
        response_json = json.loads(response.body)
        possible_nationality = max(response_json["country"], key=itemgetter("probability"))  # get the country with higher probability
        student["possible_nationality"] = possible_nationality['country_id']
        new_student = await self.settings["db"]["students"].insert_one(student)
        created_student = await self.settings["db"]["students"].find_one(
            {"_id": new_student.inserted_id}
        )
        print(f"   Added student with id: {str(student['_id'])}")
        self.set_status(201)
        return self.write(created_student)

    async def put(self, student_id):
        student = tornado.escape.json_decode(self.request.body)
        await self.settings["db"]["students"].update_one(
            {"_id": student_id}, {"$set": student}
        )
        if (
            updated_student := await self.settings["db"]["students"].find_one({"_id": student_id})
        ) is not None:
            self.status(200)
            return self.write(updated_student)
        raise tornado.web.HTTPError(404)

    async def delete(self, student_id):
        delete_result = await db["students"].delete_one({"_id": student_id})
        if delete_result.deleted_count == 1:
            self.set_status(204)
            return self.finish()
        raise tornado.web.HTTPError(404)


async def main():
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/(?P<student_id>\w+)", MainHandler)
    ], db=db)
    application.listen(9000)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
