from salesmanago_page import SalesmanagoPage


class HomePage(SalesmanagoPage):
    def accept_privacy_policy(self):
        self.click_on('//*[@id="adroll_consent_accept"]')

    def hide_live_chat(self):
        self.hide_live_chat_if_open()

    def click_on_resources(self):
        self.click_on('//*[a="resources"]')

    def click_on_ebooks(self):
        self.click_on_by_javascript('//*[@class="dropdown__element"]/a[@href="/info/knowledgecenter.htm"]')
