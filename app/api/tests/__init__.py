from flask import json, Flask
from flask.testing import FlaskClient
import unittest
from app import create_app
from config import BaseConfig


class ApiClient(FlaskClient):
    def open(self, *args, **kw):
        """
        Sends HTTP Authorization header with  the ``HTTP_AUTHORIZATION`` config value
        unless :param:`authorize` is ``False``.
        """
        headers = kw.pop('headers', [])

        if 'data' in kw and (kw.pop('force_json', False) or not isinstance(kw['data'], str)):
            kw['data'] = json.dumps(kw['data'])
            kw['content_type'] = 'application/json'

        return super(ApiClient, self).open(*args, headers=headers, **kw)


# class TestConfig(BaseConfig):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite://'
#     BCRYPT_LOG_ROUNDS = 4
#     DEBUG = True
#     API_AUTH = True
#     TEST_CLIENT_CLASS = ApiClient
#
#
# class BaseTestCase(unittest.TestCase):
#     def assertJSONEqual(self, first, second, msg=None):
#         self.assertEqual(json.loads(json.dumps(first)), json.loads(json.dumps(second)), msg)
#
#     def _without(self, dct, without):
#         return {k: v for k, v in dct.items() if k not in without}
#
#     def assertEqualWithout(self, first, second, without, msg=None):
#         if isinstance(first, list) and isinstance(second, list):
#             self.assertEqual(
#                 [self._without(v, without) for v in first],
#                 [self._without(v, without) for v in second],
#                 msg=msg
#             )
#         elif isinstance(first, dict) and isinstance(second, dict):
#             self.assertEqual(self._without(first, without),
#                              self._without(second, without),
#                              msg=msg)
#         else:
#             self.maxDiff = None
#             self.assertEqual(first, second)
#
#     def create_app(self):
#         app = create_app(TestConfig)
#         app.test_client_class = ApiClient
#         return app
#
#     def pp(self, obj):
#         print(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
