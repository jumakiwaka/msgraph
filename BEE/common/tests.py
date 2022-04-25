from django.test import TestCase
from common.logging import get_logger
import logging


class TestLogger(TestCase):
    def test_get_logger(self):
        logger = get_logger(__name__)

        self.assertEqual(type(logger), logging.Logger)
        self.assertEqual(logger.name, __name__)
