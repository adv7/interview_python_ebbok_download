from selenium import webdriver
import pathlib
import os
import csv


def initialize_driver():
    download_dir = f"{pathlib.Path().absolute()}\\downloads"
    chrome_options = webdriver.ChromeOptions()
    prefs = {"plugins.always_open_pdf_externally": True, "download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    init_driver = webdriver.Chrome(options=chrome_options)
    init_driver.get("https://www.salesmanago.com/")
    return init_driver


def get_ebook_titles(path):
    with open(path) as file:
        reader = csv.reader(file, delimiter=',')
        titles = [col1 for col1 in reader]
        return titles


class FileManager:
    def __init__(self, file):
        self.file = file

    def is_file_downloaded(self):
        print(f"is_file_name: {self.file}")
        return os.path.isfile(f"{pathlib.Path().absolute()}\\downloads\\{self.file}")

    def delete_downloaded_file(self):
        os.remove(f"{pathlib.Path().absolute()}\\downloads\\{self.file}")
