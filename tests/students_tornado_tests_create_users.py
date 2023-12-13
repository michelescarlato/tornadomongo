import asyncio
import atexit
import json
import motor
import requests
import tornado.escape
from tornado.web import Application
from bson import ObjectId, json_util
from students_tornado import MainHandler
from tornado.testing import AsyncHTTPTestCase, AsyncTestCase, AsyncHTTPClient, gen_test
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


    '''
        response = self.fetch('/6579d4950f5908701be0534c', method='DELETE')
        self.assertEqual(response.code, 404)


    #@gen_test
    def delete_nonexisting_user(self):
        response = self.fetch('/6579d4950f5908701be0534c', method='DELETE')
        self.assertEqual(response.code, 404)
        
    '''

'''
class TestDeleteNonExistingStudents(AsyncHTTPTestCase):
    def get_app(self):
        application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/(?P<student_id>\w+)", MainHandler)
        ], db=db)
        application.listen(9000)
        return application

    def test_get_students_list(self):
        response = self.fetch('/', method='GET')
        self.assertEqual(response.code, 200)
        return

    def delete_nonexisting_user(self):
        response = self.fetch('/6579d4950f5908701be0534c', method='DELETE')
        self.assertEqual(response.code, 404)
        return
    '''
'''
    
    
    def test_get_populated_students_list(self):
        response = self.fetch('/', method='GET')
        self.assertEqual(response.code, 200)
'''
'''
    def test_delete_student(self):
        response = self.fetch('/', method='GET')
        print(response.body)
'''

        #    response = self.fetch(f'/{id_to_delete}', method='DELETE')
        #    self.assertEqual(response.code, 204)


'''
    def test_http_fetch(self):
        client = AsyncHTTPClient()
        client.fetch("http://localhost:9000/")#, self.stop)
        response = self.wait()
        # Test contents of response
        self.assertEqual(response.code, 200)
        #self.assertIn("FriendFeed", response.body)




class TestStudentsTornado(AsyncHTTPTestCase):
    # def get_app(self):
    #   return students_tornado.main()
'''