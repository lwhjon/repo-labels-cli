import argparse

from utilities.cli_utils import open_link, remove_url_trailing_slash, format_url, run_extractor
from unittest import TestCase
from unittest.mock import patch


class Test(TestCase):

    @patch('webbrowser.open')
    def test_open_link_success(self, mock_web_browser_open):
        args = argparse.Namespace(url='https://github.com')
        open_link(args)
        mock_web_browser_open.assert_called_once_with('https://github.com', new=2)

    def test_remove__url_trailing_slash_input_url_with_trailing_slash_returns_input_url_without_trailing_space(self):
        test_url = 'https://github.com/'
        self.assertEqual("https://github.com", remove_url_trailing_slash(test_url))

    def test_remove_url_trailing_slash_input_url_no_trailing_slash_returns_input_url(self):
        test_url = 'https://github.com'
        self.assertEqual("https://github.com", remove_url_trailing_slash(test_url))

    def test_format_url_input_url_with_trailing_slash_returns_input_url_without_trailing_space(self):
        test_url = 'https://github.com/'
        self.assertEqual("https://github.com", format_url(test_url))

    def test_format_url_input_url_no_scheme_returns_input_url_with_prepended_https_scheme(self):
        test_url = 'github.com'
        self.assertEqual("https://github.com", format_url(test_url))

    def test_format_url_input_valid_url_returns_input_url(self):
        test_url = 'https://github.com/'
        self.assertEqual("https://github.com", format_url(test_url))

    def test_run_extractor_input_not_supported_link_returns_none_and_log_site_not_supported_error_msg(self):
        with self.assertLogs('utilities.extractor_facade', level='ERROR') as cm:
            response = run_extractor('https://notsupported.com/repoowner/repo')
        self.assertIs(None, response)
        self.assertEqual(
            "ERROR:utilities.extractor_facade:SiteNotSupported: notsupported.com Repository host not supported.",
            cm.output[len(cm.output) - 1])
