from pages.home_page import HomePage
from pages.ebooks_list_page import EbooksListPage
from pages.data_form_page import DataFormPage
from utilities import initialize_driver, FileManager, get_ebook_titles
from parameterized import parameterized
import unittest
import time


class TestEbookDownloading(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        driver = initialize_driver()
        home_page = HomePage(driver)
        home_page.accept_privacy_policy()
        time.sleep(2)
        home_page.hide_live_chat()
        home_page.click_on_resources()
        home_page.click_on_ebooks()

        cls.ebook_list_page = EbooksListPage(driver)
        cls.data_form_page = DataFormPage(driver)

    def setUp(self) -> None:
        self.data_form_page.close_tab_with_index_if_more_than_one(1)
        self.data_form_page.switch_to_tab(0)
        self.ebook_list_page.navigate("https://www.salesmanago.com/info/knowledgecenter.htm")

    @parameterized.expand(get_ebook_titles('../ebook_titles.csv'))
    def test_is_title_exist(self, title):
        assert self.ebook_list_page.is_searched_title_available(title) is not None

    @parameterized.expand(get_ebook_titles('../ebook_titles.csv'))
    def test_ebook_download(self, test_input):
        self.ebook_list_page.select_ebook_to_download(test_input)
        self.ebook_list_page.switch_to_tab(1)

        time.sleep(2)
        self.data_form_page.hide_live_chat_if_open()
        self.data_form_page.submit_data_form()
        time.sleep(4)
        file_name = self.data_form_page.get_file_name()
        self.data_form_page.download_pdf_file()
        time.sleep(5)

        fm = FileManager(file_name)
        assert fm.is_file_downloaded() is True
        fm.delete_downloaded_file()
