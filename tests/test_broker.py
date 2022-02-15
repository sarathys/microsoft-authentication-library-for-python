from tests import unittest
import logging
import sys

if not sys.platform.startswith("win"):
    raise unittest.SkipTest("Currently, our broker supports Windows")
from msal.broker import (  # Import them after the platform check
    _signin_interactively, _acquire_token_silently, RedirectUriError)


logging.basicConfig(level=logging.DEBUG)

class BrokerTestCase(unittest.TestCase):
    """These are the unit tests for the thin broker.py layer.

    It currently hardcodes some test apps which might be changed/gone in the future.
    The existing test_e2e.py is sophisticated to pull test configuration securely from lab.
    """
    _client_id = "26a7ee05-5602-4d76-a7ba-eae8b7b67941"  # A pre-configured test app
    _authority = "https://login.microsoftonline.com/common"
    _scopes = ["https://graph.microsoft.com/.default"]

    def test_interactive_then_silent(self):
        result = _signin_interactively(self._authority, self._client_id, self._scopes)
        self.assertIsNotNone(result.get("access_token"), result)

        account_id = result["_account_id"]
        result = _acquire_token_silently(
                self._authority, self._client_id, account_id, self._scopes)
        self.assertIsNotNone(result.get("access_token"), result)

    def test_unconfigured_app_should_raise_exception(self):
        app_without_needed_redirect_uri = "289a413d-284b-4303-9c79-94380abe5d22"
        with self.assertRaises(RedirectUriError):
            _signin_interactively(self._authority, app_without_needed_redirect_uri, self._scopes)
        # Note: _acquire_token_silently() would raise same exception,
        #       we skip its test here due to the lack of a valid account_id

    def test_signin_interactively_and_select_account(self):
        print("An account picker UI will pop up. See whether the auth result matches your account")
        result = _signin_interactively(
            self._authority, self._client_id, self._scopes, prompt="select_account")
        self.assertIsNotNone(result.get("access_token"), result)
        if "access_token" in result:
            result["access_token"] = "********"
        import pprint; pprint.pprint(result)
