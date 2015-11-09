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

        # property details
        property_details_section = properties_section.find_element_by_id("property-details-section")
        property_details_header = property_details_section.find_element_by_tag_name("h2")
        self.assertEqual(property_details_header.text, "Property Details")
        property_details_table = property_details_section.find_element_by_tag_name("table")
        rows = property_details_table.find_elements_by_tag_name("tr")

        name_label = rows[0].find_element_by_tag_name("th").text
        postcode_label = rows[1].find_element_by_tag_name("th").text
        type_label = rows[2].find_element_by_tag_name("th").text

        self.assertEqual(name_label, "Name")
        self.assertEqual(postcode_label, "Postcode")
        self.assertEqual(type_label, "Type")

        name = rows[0].find_element_by_tag_name("td")
        postcode = rows[1].find_element_by_tag_name("td")
        type_ = rows[2].find_element_by_tag_name("td")

        property_selectors[0].click()
        self.assertEqual(name.text, "Property1")
        self.assertEqual(postcode.text, "HA0 1AA")
        self.assertEqual(type_.text, "Terrace")

        property_selectors[1].click()
        self.assertEqual(name.text, "Property2")
        self.assertEqual(postcode.text, "HA0 1AB")
        self.assertEqual(type_.text, "Semi-Detached")
        
        property_selectors[2].click()
        self.assertEqual(name.text, "Property3")
        self.assertEqual(postcode.text, "HA0 1AN")
        self.assertEqual(type_.text, "Flat")
        
        # check data section exists
        data_section = self.browser.find_element_by_id('data-section')
        data_section_header = data_section.find_element_by_tag_name('h2')
        self.assertEqual(data_section_header.text, 'Data')

        # check filter section
        filter_section = data_section.find_element_by_id("data-filter-section")
        filter_form = filter_section.find_element_by_tag_name("form")
        first_date_input = filter_form.find_element_by_css_selector('input[name="first-date"]')
        last_date_input = filter_form.find_element_by_css_selector('input[name="last-date"]')
        sensor_input = filter_form.find_element_by_css_selector('select[name="sensor"]')
        submit = filter_form.find_element_by_css_selector('input[type="submit"]')

        property_selectors[0].click()
        sensor_options = sensor_input.find_elements_by_tag_name("option")
        self.assertEqual(sensor_options[0].text, "0")
        self.assertEqual(sensor_options[1].text, "1")

        # data table section
        class DataTable:
            def __init__(self):
                self.div = data_section.find_element_by_css_selector("div#data-table-div")
                self.table = self.div.find_element_by_css_selector("table#data-table")
            def rows(self, exclude_headers=False):
                rows = self.table.find_elements_by_tag_name("tr")
                return rows[1 if exclude_headers else 0:]

        data_table = DataTable()
        rows = data_table.rows(exclude_headers=True)
        self.assertEqual(len(rows), 3)
        # for row in rows:
        #     (datetime, temperature, humidity, light, occupancy, battery) = [td.text for td in row.find_elements_by_tag_name("td")]

        # graph section
        class GraphSection:
            def __init__(self):
                self.section = data_section.find_element_by_css_selector("section#graph-section")
                self.quantity_selector = self.section.find_element_by_css_selector("select#quantity-selector")
                self.div = self.section.find_element_by_css_selector("div#graph-div")
                self.graph = self.div.find_element_by_css_selector("svg")

        graph_section = GraphSection()

        selected_option = graph_section.quantity_selector.find_element_by_css_selector("option:checked")
        self.assertEqual(selected_option.text, "Temperature")
        options = graph_section.quantity_selector.find_elements_by_tag_name("option")
        self.assertEqual(len(options), 3)
        self.assertEqual(options[0].text, "Temperature")
        self.assertEqual(options[1].text, "Humidity")
        self.assertEqual(options[2].text, "Light")

        # graph has loaded
        self.assertNotEqual(len(graph_section.graph.find_elements_by_css_selector("*")), 0)
        
        self.fail('TODO')
