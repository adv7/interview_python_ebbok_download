from pages.salesmanago_page import SalesmanagoPage


class HomePage(SalesmanagoPage):
    XPATH_PRIVACY_POLICY_ACCEPT_BTN = '//*[@id="adroll_consent_accept"]'
    XPATH_RESOURCES = '//*[a="resources"]'
    XPATH_EBOOKS = '//*[@class="dropdown__element"]/a[@href="/info/knowledgecenter.htm"]'

    def accept_privacy_policy(self):
        if self.check_element_exists_by_xpath(self.XPATH_PRIVACY_POLICY_ACCEPT_BTN):
            self.click_on(self.XPATH_PRIVACY_POLICY_ACCEPT_BTN)

    def hide_live_chat(self):
        self.hide_live_chat_if_open()

    def click_on_resources(self):
        self.click_on(self.XPATH_RESOURCES)

    def click_on_ebooks(self):
        self.click_on_by_javascript(self.XPATH_EBOOKS)
