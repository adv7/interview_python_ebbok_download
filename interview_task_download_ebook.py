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
        self.driver.find_element_by_xpath(locator).click()

    def click_on_by_javascript(self, locator):
        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath(locator))

    def click_element_found_by_url(self, locator):
        self.driver.find_element_by_xpath('//a[@href="' + locator + '"]').click()

    def switch_to_iframe(self, locator):
        self.driver.switch_to.frame(self.driver.find_element_by_xpath(locator))

    def switch_to_default(self):
        self.driver.switch_to.default_content()

    def switch_to_tab(self, tab_index):
        self.driver.switch_to.window(self.driver.window_handles[tab_index])

    def check_element_exists_by_xpath(self, locator):
        try:
            return bool(self.driver.find_element_by_xpath(locator))
        except NoSuchElementException:
            return False

    def get_single_attribute_value(self, locator, attribute):
        return self.driver.find_element_by_xpath(locator).get_attribute(attribute)

    def get_all_attributes_by_class_name(self, locator):
        attribute_name = self.get_attribute_name(locator)

        elements_list = self.driver.find_elements_by_class_name(locator)
        attribute_values_list = [element.get_attribute(attribute_name) for element in elements_list]
        return attribute_values_list

    @staticmethod
    def get_attribute_name(locator):
        attribute_name = re.search(r"\[\w+\]", locator).group(0).replace("[", "").replace("]", "")
        if len(attribute_name) > 0:
            return attribute_name
        return ""

    def enter_data_to_form_field(self, locator, value):
        self.driver.find_element_by_xpath(locator).send_keys(value)

    def close_browser(self):
        self.driver.quit()


class SalesmanagoPage(BasePage):
    def hide_live_chat_if_open(self):
        if self.check_element_exists_by_xpath('//iframe[@class="bhr-chat__messenger"]'):
            self.switch_to_iframe('//iframe[@class="bhr-chat__messenger"]')
            self.click_on('//*[@class="bhr-chat-messenger__minimalise"]')
            self.switch_to_default()


class HomePage(SalesmanagoPage):
    def accept_privacy_policy(self):
        self.click_on('//*[@id="adroll_consent_accept"]')

    def hide_live_chat(self):
        self.hide_live_chat_if_open()

    def click_on_resources(self):
        self.click_on('//*[a="resources"]')

    def click_on_ebooks(self):
        self.click_on_by_javascript('//*[@class="dropdown__element"]/a[@href="/info/knowledgecenter.htm"]')


class EbooksListPage(BasePage):
    def get_ebook_urls_list(self):
        return self.get_all_attributes_by_class_name('ebook__img--container [href]')

    def is_searched_title_available(self, user_input_ebook_title):
        # TEST IS EBOOK WITH GIVEN TITLE EXIST
        for url_with_title in self.get_ebook_urls_list():
            raw_title = re.sub(r"(https://)(www\.)*(salesmanago.com/info/)", "", url_with_title).replace(".htm",
                                                                                                         "").replace(
                "_", " ").replace("-", " ")

            # print(f"title:\t{raw_title}")
            if str(user_input_ebook_title).upper() == str(raw_title).upper():
                return url_with_title

        return None

    def select_ebook_to_download(self, user_input_ebook_title):
        self.click_element_found_by_url(self.is_searched_title_available(user_input_ebook_title))


class DataFormPage(SalesmanagoPage):
    def get_button_locations_dependent_on_form_types(self):
        if self.check_element_exists_by_xpath("//*[@class=\"btn center-block form-btn form-btn\" and @type=\"submit\"]"):
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

        self.hide_live_chat_if_open()
        if self.check_element_exists_by_xpath('//*[@class="quote__content"]'):
            self.click_on('//*[@class="quote__close"]')

        self.click_on(self.get_button_locations_dependent_on_form_types()[0])

    def get_file_name(self):
        file_url = self.get_single_attribute_value(self.get_button_locations_dependent_on_form_types()[1], "href")
        return re.search(r"/\w+\.pdf", file_url).group(0).replace("/", "")

    def download_pdf_file(self):
        # WHEN OPENING FILE DOWNLOAD STARTS AUTOMATICALLY (WEBDRIVER SETTINGS)
        self.click_on_by_javascript(self.get_button_locations_dependent_on_form_types()[1])
        # WAIT TIL DOWNLOAD PROCESS ENDS


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
        home_page = HomePage(driver)
        home_page.accept_privacy_policy()
        time.sleep(2)
        home_page.hide_live_chat()
        home_page.click_on_resources()
        home_page.click_on_ebooks()

        cls.ebook_list_page = EbooksListPage(driver)
        cls.data_form_page = DataFormPage(driver)

    def test_1_is_title_exist(self):
        self.assertIsNotNone(self.ebook_list_page.is_searched_title_available(self.searched_ebook_title))

    def test_2_ebook_download(self):
        self.ebook_list_page.select_ebook_to_download(self.searched_ebook_title)
        self.ebook_list_page.switch_to_tab(1)

        self.data_form_page.submit_data_form()

        time.sleep(5)
        file_name = self.data_form_page.get_file_name()
        self.data_form_page.download_pdf_file()
        time.sleep(10)
        self.data_form_page.close_browser()

        fm = FileManager(file_name)
        self.assertTrue(fm.is_file_downloaded())
        fm.delete_downloaded_file()


if __name__ == '__main__':
    unittest.main()
