import json
import motor
import tornado.escape
from tornado.web import Application
from students_tornado import MainHandler
from tornado.testing import AsyncHTTPTestCase
import tornado.web

uri = 'mongodb://root:example@172.20.0.2:27017/'
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.universityTests


class TestCreateStudentsList(AsyncHTTPTestCase):
    def get_app(self):
        application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/(?P<student_id>\w+)", MainHandler)
        ], db=db)
        application.listen(9000)
        return application

    def test_create_student(self):
        with open('../db-schemas/students-objects.json', 'r') as f:
            data = json.load(f)
        for student in data['students']:
            print(student)
            student = json.dumps(student)
            response = self.fetch('/', method='POST', body=student)
            self.assertEqual(response.code, 201)
