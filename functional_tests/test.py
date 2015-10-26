import os
import sys
import time
from datetime import datetime
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_WAIT = 5

def get_classes(element):
    return element.get_attribute('class').split(' ')

def has_class(class_, element):
    return class_ in get_classes(element)

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
        self.browser.quit()

    def test(self):
        
        self.browser.get(self.live_server_url)

        # check page title
        self.assertIn('OpenTRV Brent Trial', self.browser.title)

        # check properties section exists
        properties_section = self.browser.find_element_by_id('properties-section')
        properties_header = properties_section.find_element_by_tag_name('h2')
        self.assertEqual(properties_header.text, 'Properties')

        property_selection_section = properties_section.find_element_by_id('property-selection-section')
        property_selectors = property_selection_section.find_elements_by_tag_name('button')
        self.assertEqual(len(property_selectors), 3)
        self.assertEqual(property_selectors[0].text, 'Property1')
        self.assertEqual(property_selectors[1].text, 'Property2')
        self.assertEqual(property_selectors[2].text, 'Property3')
        self.assertTrue(has_class('selected', property_selectors[0]))

        # user clicks button 2
        property_selectors[1].click()
        self.assertFalse(has_class('selected', property_selectors[0]))
        self.assertTrue(has_class('selected', property_selectors[1]))
        
        # user clicks button 3
        property_selectors[2].click()
        self.assertFalse(has_class('selected', property_selectors[0]))
        self.assertFalse(has_class('selected', property_selectors[1]))
        self.assertTrue(has_class('selected', property_selectors[2]))
        
        self.fail('TODO')
