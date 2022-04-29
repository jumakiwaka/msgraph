from django.test import TestCase
from common.test_utils import create_test_user_token

class LoginAPIVIEWTestCase(TestCase):
    def setUp(self):
        self.url = "/auth/login"
        self.token = create_test_user_token()


    def test_login_api_400(self):
        res = self.client.post(self.url)

        self.assertEqual(res.status_code, 400)

    def test_login_api_invalid_code(self):
        data = {
            "code" : "jdjdjksksjdjdjddk"
        }
        res = self.client.post(self.url, data)
        res_json = res.json()

        self.assertEqual(res.status_code, 400)
        self.assertIsNotNone(res_json.get("error"))
        self.assertIn('Invalid request', res_json.get('error'))
