from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import re
import unittest
import time
import pathlib
import os


def initialize_driver():
    download_dir = f"{pathlib.Path().absolute()}\\downloads"
    chrome_options = webdriver.ChromeOptions()
    prefs = {"plugins.always_open_pdf_externally": True, "download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    chromedriver = r'C:\Users\kryst\OneDrive\Dokumenty\selenium_drivers\chromedriver.exe'
    init_driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)
    init_driver.get("https://www.salesmanago.com/")
    return init_driver


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click_on(self, locator):
        try:
            self.driver.find_element_by_xpath(locator).click()
        except NoSuchElementException:
            print(f"msg: element with xpath: {locator} wasn't found")

    def click_on_by_javascript(self, locator):
        try:
            self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath(locator))
        except NoSuchElementException:
            print(f"msg: element with xpath: {locator} wasn't found")

    def is_xpath_exist(self, locator):
        elements_list = self.driver.find_elements_by_xpath(locator)
        if len(elements_list) > 0:
            return True
        return False

    def get_single_attribute_value(self, locator, attribute):
        try:
            return self.driver.find_element_by_xpath(locator).get_attribute(attribute)
        except NoSuchElementException:
            print(f"msg: element with xpath: {locator} wasn't found")

    def get_all_attributes_by_class_name(self, locator):
        try:
            attribute_name = self.get_attribute_name(locator)

            elements_list = self.driver.find_elements_by_class_name(locator)
            attribute_values_list = [element.get_attribute(attribute_name) for element in elements_list]
            return attribute_values_list
        except NoSuchElementException:
            print(f"msg: elements with specified class name: {locator} weren't found")

    @staticmethod
    def get_attribute_name(locator):
        try:
            return re.search(r"\[\w+\]", locator).group(0).replace("[", "").replace("]", "")
        except AttributeError:
            return ""

    def choose_element_by_url(self, locator):
        try:
            self.driver.find_element_by_xpath('//a[@href="' + locator + '"]').click()
        except NoSuchElementException:
            print(f"msg: element with specified url: {locator} wasn't found")

    def switch_to_tab(self, tab_index):
        self.driver.switch_to.window(self.driver.window_handles[tab_index])

    def enter_data_to_form_field(self, locator, value):
        try:
            self.driver.find_element_by_xpath(locator).send_keys(value)
        except NoSuchElementException:
            print(f"msg: element with specified xpath: {locator} wasn't found")

    def close_browser(self):
        self.driver.quit()


class HomePage(BasePage):
    def accept_privacy_policy(self):
        self.click_on('//*[@id="adroll_consent_accept"]')

    def hide_live_chat(self):
        self.click_on('//*[@id="bhr-chat-frame-body"]/div/div')

    def click_on_resources(self):
        self.click_on('//*[@class="custom-lowbar__link active-menu-item"]')

    def click_on_ebooks(self):
        self.click_on_by_javascript('//*[@class="dropdown__element"]/a[@href="/info/knowledgecenter.htm"]')


class EbooksListPage(BasePage):
    def get_ebook_urls_list(self):
        return self.get_all_attributes_by_class_name('ebook__img--container [href]')

    """ TEST IS EBOOK WITH GIVEN TITLE EXIST """
    """ ebook live chat - existed title to test """

    def is_searched_title_available(self, user_input_ebook_title):
        for url_with_title in self.get_ebook_urls_list():
            raw_title = re.sub(r"(https://)(www\.)*(salesmanago.com/info/)", "", url_with_title).replace(".htm",
                                                                                                         "").replace(
                "_", " ").replace("-", " ")

            # print(f"title:\t{raw_title}")
            if str(user_input_ebook_title).upper() == str(raw_title).upper():
                return url_with_title

        return None

    def select_ebook_to_download(self, user_input_ebook_title):
        self.choose_element_by_url(self.is_searched_title_available(user_input_ebook_title))


class DataFormPage(BasePage):
    def get_button_locations_dependent_on_form_types(self):
        if self.is_xpath_exist("//*[@class=\"btn center-block form-btn form-btn\" and @type=\"submit\"]"):
            return ("//*[@class=\"btn center-block form-btn form-btn\" and @type=\"submit\"]",
                    "//*[@class=\"thanks-message\"]/div/a[contains(@href, \".pdf\")]")
        else:
            return ("//*[@class=\"btn btn-success\"]",
                    "//*[@class=\"ebookcontainer__img--buttoncontainer-button\"]")

    def submit_data_form(self):
        self.enter_data_to_form_field("//*[@class=\"form-control\" and @name=\"name\"]", "test")
        self.enter_data_to_form_field("//*[@class=\"form-control\" and @name=\"email\"]",
                                      f"benhauer+test_{datetime.now().timestamp()}@qafake.pl")
        self.enter_data_to_form_field("//*[@class=\"form-control\" and @name=\"company\"]", "company")
        self.enter_data_to_form_field("//*[@class=\"form-control\" and @name=\"url\"]", "https://google.com")
        self.enter_data_to_form_field("//*[@class=\"form-control\" and @name=\"phoneNumber\"]", "123123123")
        self.click_on(self.get_button_locations_dependent_on_form_types()[0])

    def get_file_name(self):
        file_url = self.get_single_attribute_value(self.get_button_locations_dependent_on_form_types()[1], "href")
        return re.search(r"/\w+\.pdf", file_url).group(0).replace("/", "")

    """ WHEN OPENING FILE DOWNLOAD STARTS AUTOMATICALLY (WEBDRIVER SETTINGS) """

    def download_pdf_file(self):
        self.click_on_by_javascript(self.get_button_locations_dependent_on_form_types()[1])
        """ WAIT TIL DOWNLOAD PROCESS ENDS """


class FileManager:
    def __init__(self, file):
        self.file = file

    def is_file_downloaded(self):
        return os.path.isfile(f"{pathlib.Path().absolute()}\\downloads\\{self.file}")

    def delete_downloaded_file(self):
        os.remove(f"{pathlib.Path().absolute()}\\downloads\\{self.file}")


class TestEbookDownloading(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.searched_ebook_title = input("Enter ebook title: ")
        driver = initialize_driver()
        cls.hp = HomePage(driver)
        cls.elp = EbooksListPage(driver)
        cls.dfp = DataFormPage(driver)

    def test_1_is_title_exist(self):
        self.hp.accept_privacy_policy()
        self.hp.hide_live_chat()
        self.hp.click_on_resources()
        self.hp.click_on_ebooks()

        self.assertIsNotNone(self.elp.is_searched_title_available(self.searched_ebook_title))

    def test_2_ebook_download(self):
        # self.hp.accept_privacy_policy()
        # self.hp.hide_live_chat()
        # self.hp.click_on_resources()
        # self.hp.click_on_ebooks()

        self.elp.select_ebook_to_download(self.searched_ebook_title)
        self.elp.switch_to_tab(1)

        self.dfp.submit_data_form()

        time.sleep(5)
        file_name = self.dfp.get_file_name()
        # print(file_name)
        self.dfp.download_pdf_file()
        time.sleep(10)
        self.dfp.close_browser()

        fm = FileManager(file_name)
        # print(f"is exist file: {fm.is_file_downloaded()}")
        self.assertTrue(fm.is_file_downloaded())
        fm.delete_downloaded_file()


if __name__ == '__main__':
    unittest.main()
