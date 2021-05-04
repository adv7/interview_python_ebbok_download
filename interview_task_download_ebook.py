from pages.home_page import HomePage
from pages.ebooks_list_page import EbooksListPage
from pages.data_form_page import DataFormPage
from selenium import webdriver
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
