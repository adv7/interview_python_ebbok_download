from pages.base_page import BasePage


class SalesmanagoPage(BasePage):
    def hide_live_chat_if_open(self):
        if self.check_element_exists_by_xpath('//iframe[@class="bhr-chat__messenger"]'):
            self.switch_to_iframe('//iframe[@class="bhr-chat__messenger"]')
            self.click_on('//*[@class="bhr-chat-messenger__minimalise"]')
            self.switch_to_default()
