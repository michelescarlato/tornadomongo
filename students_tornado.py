import asyncio
import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.log import enable_pretty_logging
from logging import getLogger, FileHandler, INFO
import motor.motor_asyncio
import motor.motor_tornado
from tornado.httpclient import AsyncHTTPClient
from bson import ObjectId
from operator import itemgetter
import os
from dotenv import load_dotenv

enable_pretty_logging()
log_file = "students_tornado.log"
handler = FileHandler("logs/"+log_file)
logger = getLogger("tornado.access")  # per-request logging for tornado's HTTP servers
logger.addHandler(handler)
logger.setLevel(INFO)

load_dotenv()
uri = os.getenv('URI')
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.university


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')
        self.set_header("Accept-Charset", 'utf-8')

    async def get(self, student_id=None):
        if student_id is not None:
            if (student := await self.settings["db"]["students"].find_one({"_id": student_id})) is not None:
                self.write(student)
                logger.info(f"Get student from the db with id: {student_id}")
            else:
                raise tornado.web.HTTPError(404)
        else:
            students = await self.settings["db"]["students"].find().to_list(1000)
            self.set_status(200)
            logger.info(f"Get student list from the db. Total number of students {len(students[0])}.")
            self.write(tornado.escape.json_encode({"students": students}))  # escape characters
        await self.finish()

    async def post(self):
        student = tornado.escape.json_decode(self.request.body)
        student["_id"] = str(ObjectId())
        logger.info(f"Adding student with id: {str(student['_id'])}")
        url = f'https://api.nationalize.io/?name={student["name"]}'
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url)
        response_json = tornado.escape.json_decode(response.body)
        # get the country with higher probability
        possible_nationality = max(response_json["country"], key=itemgetter("probability"))
        student["possible_nationality"] = possible_nationality['country_id']
        new_student = await self.settings["db"]["students"].insert_one(student)
        if (created_student := await self.settings["db"]["students"].
                find_one({"_id": new_student.inserted_id})) is not None:
            logger.info(f"Added student with id: {str(student['_id'])}")
            self.set_status(201)
            self.write(tornado.escape.json_encode(created_student))
            await self.finish()
        else:
            raise tornado.web.HTTPError(404)

    async def put(self, student_id):
        student = tornado.escape.json_decode(self.request.body)
        await self.settings["db"]["students"].update_one(
            {"_id": student_id}, {"$set": student}
        )
        if (
            updated_student := await self.settings["db"]["students"].find_one({"_id": student_id})
        ) is not None:
            self.set_status(200)
            logger.info(f"Modified student with id: {student_id}")
            self.write(tornado.escape.json_encode(updated_student))
            await self.finish()
        else:
            raise tornado.web.HTTPError(404)

    async def delete(self, student_id):
        delete_result = await self.settings["db"]["students"].delete_one({"_id": student_id})
        if delete_result.deleted_count == 1:
            self.set_status(204)
            logger.info(f"Deleted student with id: {student_id}")
            await self.finish()
        else:
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
