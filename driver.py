from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import os
from dotenv import load_dotenv
from parsel import Selector


class web_driver:
    def __init__(self, url, record_count):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        options = Options()
        options.headless = True  # hide GUI
        options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
        options.add_argument("start-maximized")  # ensure window is full-screen
        # configure chrome browser to not load images and javascript
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2}
        )

        self.driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
        self.driver.get(url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        self.load_env_vars()
        self.record_num = record_count
        self.page_loader()

    def load_env_vars(self):
        dotenv_path = Path('./app.env')
        load_dotenv(dotenv_path=dotenv_path)
        self.refence_path = os.getenv('REF_PATH')
        self.target_path = self.refence_path.format(item="*")
        self.valid_path = os.getenv("VALID_PATH")
        self.selection_path = os.getenv("SELECT_PATH")

    def get_elements(self, path):
        return self.driver.find_elements(By.XPATH, path)

    def is_validate_record(self, item):

        return not "ناموجود" in self.driver.find_elements(By.XPATH, self.valid_path.format(item=item))[0].text

    def page_loader(self):
        while True:
            # Scroll down to bottom
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            new_height = last_height
            step = 0
            while new_height == last_height and step < 100:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight+100)")
                self.driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight+300)")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight+300)")
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                step += 1

            item_cnt = len(self.get_elements(self.target_path))
            if not self.is_validate_record(item_cnt) or self.record_num <= item_cnt:
                self.record_num = min(self.record_num, item_cnt)
                while not self.is_validate_record(self.record_num):
                    self.record_num -= 1
                break

            # Wait to load page
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # break condition
            if new_height == last_height:
                break

    def go_back(self):
        self.driver.back()

    def go_link(self, link):
        self.driver.get(link)

    def get_slector(self):
        sel = Selector(text=self.driver.page_source)
        return sel.xpath(self.selection_path)
