# -*- coding: utf-8 -*-

import unittest

from selenium.webdriver.firefox import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.WebDriver()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_it_worked(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Welcome to Django', self.browser.title)


class HomeNewVisitor(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.WebDriver()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("Wappa", self.browser.title)

    def test_h1_css(self):
        self.browser.get(self.get_full_url("home"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"),
                         "rgba(200, 50, 255, 1)")


if __name__ == '__main__':
    unittest.main(warnings='ignore')
