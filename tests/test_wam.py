from tests import unittest
import logging

from msal.wam import *


logging.basicConfig(level=logging.DEBUG)

class TestWam(unittest.TestCase):
    client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # A well-known app

    def test_acquire_token_interactive(self):
        result = acquire_token_interactive(
            "https://login.microsoftonline.com/common",
            "26a7ee05-5602-4d76-a7ba-eae8b7b67941",
            ["https://graph.microsoft.com/.default"],
            )
        self.assertIsNotNone(result.get("access_token"))

    def test_acquire_token_silent(self):
        result = acquire_token_silent(
            "https://login.microsoftonline.com/common",
            "26a7ee05-5602-4d76-a7ba-eae8b7b67941",
            ["https://graph.microsoft.com/.default"],
            #{"some_sort_of_id": "placeholder"},  # TODO
            )
        self.assertIsNotNone(result.get("access_token"))
