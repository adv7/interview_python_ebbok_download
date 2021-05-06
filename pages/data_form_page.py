from pages.salesmanago_page import SalesmanagoPage
from datetime import datetime
import re


class DataFormPage(SalesmanagoPage):
    XPATH_SUBMIT_1 = '//*[@class="btn center-block form-btn form-btn" and @type="submit"]'
    XPATH_SUBMIT_2 = '//*[@class="btn btn-success"]'
    XPATH_OPEN_PDF_BUTTON_1 = '//*[@class="thanks-message"]/div/a[contains(@href, ".pdf")]'
    XPATH_OPEN_PDF_BUTTON_2 = '//*[@class="ebookcontainer__img--buttoncontainer-button"]'
    XPATH_FORM_NAME = '//*[@class="form-control" and @name="name"]'
    XPATH_FORM_EMAIL = '//*[@class="form-control" and @name="email"]'
    XPATH_FORM_COMPANY = '//*[@class="form-control" and @name="company"]'
    XPATH_FORM_URL = '//*[@class="form-control" and @name="url"]'
    XPATH_FORM_PHONE_NO = '//*[@class="form-control" and @name="phoneNumber"]'

    def get_button_locations_dependent_on_form_types(self):
        if self.check_element_exists_by_xpath(self.XPATH_SUBMIT_1):
            return self.XPATH_SUBMIT_1, self.XPATH_OPEN_PDF_BUTTON_1
        else:
            return self.XPATH_SUBMIT_2, self.XPATH_OPEN_PDF_BUTTON_2

    def submit_data_form(self):
        self.enter_data_to_form_field(self.XPATH_FORM_NAME, "test")
        self.enter_data_to_form_field(self.XPATH_FORM_EMAIL,
                                      f"benhauer+test_{round(datetime.now().timestamp())}@qafake.pl")
        self.enter_data_to_form_field(self.XPATH_FORM_COMPANY, "company")
        self.enter_data_to_form_field(self.XPATH_FORM_URL, "https://google.com")
        self.enter_data_to_form_field(self.XPATH_FORM_PHONE_NO, "123123123")

        self.hide_live_chat_if_open()
        self.hide_daily_quote_if_open()

        self.click_on(self.get_button_locations_dependent_on_form_types()[0])

    def get_file_name(self):
        file_url = self.get_single_attribute_value(self.get_button_locations_dependent_on_form_types()[1], "href")
        file_name = re.search(r"/([\w()+-])+\.pdf", file_url).group(0).replace("/", "")
        print(f"file name: {file_name}")
        return file_name

    def download_pdf_file(self):
        # WHEN OPENING FILE DOWNLOAD STARTS AUTOMATICALLY (WEBDRIVER SETTINGS)
        self.click_on_by_javascript(self.get_button_locations_dependent_on_form_types()[1])
        # WAIT TIL DOWNLOAD PROCESS ENDS
