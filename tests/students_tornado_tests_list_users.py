import motor
import tornado.escape
from tornado.web import Application
from students_tornado import MainHandler
from tornado.testing import AsyncHTTPTestCase
import tornado.web
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('URI')
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.universityTests


class TestGetStudentsList(AsyncHTTPTestCase):
    def get_app(self):
        application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/(?P<student_id>\w+)", MainHandler)
        ], db=db)
        application.listen(9000)
        return application

    def test_get_students_list(self):
        response = self.fetch('/', method='GET')
        print(response.body)
        self.assertEqual(response.code, 200)
