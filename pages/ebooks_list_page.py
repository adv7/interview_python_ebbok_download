from salesmanago_page import SalesmanagoPage
import re


class EbooksListPage(SalesmanagoPage):
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
