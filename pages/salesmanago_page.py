from pages.base_page import BasePage


class SalesmanagoPage(BasePage):
    XPATH_CHAT_IFRAME = '//iframe[@class="bhr-chat__messenger"]'
    XPATH_CHAT_MINIMALISE_BTN = '//*[@class="bhr-chat-messenger__minimalise"]'
    XPATH_DAILY_QUOTE_CONTENT = '//*[@class="quote__content"]'
    XPATH_DAILY_QUOTE_CLOSE_BTN = '//*[@class="quote__close"]'

    def hide_live_chat_if_open(self):
        if self.check_element_exists_by_xpath(self.XPATH_CHAT_IFRAME):
            self.switch_to_iframe(self.XPATH_CHAT_IFRAME)
            self.click_on(self.XPATH_CHAT_MINIMALISE_BTN)
            self.switch_to_default()

    def hide_daily_quote_if_open(self):
        if self.check_element_exists_by_xpath(self.XPATH_DAILY_QUOTE_CONTENT):
            self.click_on(self.XPATH_DAILY_QUOTE_CLOSE_BTN)
