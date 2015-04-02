import unittest
from app import app
from route import ApiRoutes

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_health_check(self):
        result = self.app.get(ApiRoutes.ApiRoutesConst.HEALTH_CHECK)
        ''':type result: flask.Response'''
        self.assertEqual(result.status_code, 200, "Healthcheck HTTP status should be 200")
