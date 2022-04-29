from django.test import TestCase
from common.test_utils import create_test_user_token
class DashBoardViewTestCase(TestCase):
    def setUp(self):
        self.url = "/dashboard/summary"
        self.token = create_test_user_token()

    def test_dashboard_summary_api_401(self):
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, 401)

    def test_dashboard_summary_api_404(self):
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Token {self.token}"
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, 404)
