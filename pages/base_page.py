from selenium.common.exceptions import NoSuchElementException
import re


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
