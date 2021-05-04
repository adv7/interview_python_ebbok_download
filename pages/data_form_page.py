from salesmanago_page import SalesmanagoPage
import datetime
import re


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
