from unidecode import unidecode
import re
from pathlib import Path
import os
from dotenv import load_dotenv
from driver import webdriver


def char_2_num(inp):
    keys = ["یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه", "ده"]
    vals = [i for i in range(1, 11)]
    dic = dict(zip(keys, vals))
    inp = inp.split(" ")
    r = 0
    for i in inp:
        r += dic.get(i, 0)
        if i == "نیم":
            r += 0.5
    return r


class info_extraction:
    def __init__(self, driver: webdriver):
        self.driver_update(driver)
        dotenv_path = Path('./app.env')
        load_dotenv(dotenv_path=dotenv_path)
        self.static_path = {
            "model": os.getenv('MODEL_PATH'),
            "capacity": os.getenv('CAPACITY_PATH')}
        self.base_dynamic_path = os.getenv('DYBASE_PATH')
        self.dynamic_path = {"shop": os.getenv('SHOP'),
                             "price": os.getenv('PRICE')}

    def driver_update(self, driver):
        self.driver = driver

    def get_path(self, key: str, item=None, is_dynamic=True, ):
        if self.driver is None:
            return []
        if self.dynamic_path.get(key, None) is not None and is_dynamic:
            sub_path = self.dynamic_path.get(key, None)
            if sub_path is None:
                return None
            path = self.base_dynamic_path.format(item=item) + sub_path
        else:
            path = self.static_path.get(key, None)
            if path is None:
                return None
        if self.validate_path(path):

            return path
        else:
            return None

    def validate_path(self, path: str):
        element_list = self.driver.get_elements(path)
        return len(element_list) > 0

    def value_extractor(self, key: str, item=None):
        path = self.get_path(key, item=item)
        if path is None:
            return None

        text = self.driver.get_elements(path)[0].text
        if "تومان" in text:
            return int(''.join([i for i in unidecode(text.split("تومان")[0]) if i.isdigit()]))
        elif key == "capacity":
            start = re.search("ظرفیت", text)
            if start is not None:
                start = start.span()[1]
            for measure in ["گیگابایت", "گیگ", "ترابایت", "TB", "GB"]:
                end = re.search(measure, text)
                if end is None:
                    continue
                end = end.span()[0]
                if start is None:
                    start = end - 3

                text = text[start:end]
                try:
                    r = int(''.join([i for i in unidecode(text) if i.isdigit()]))
                except:
                    r = char_2_num(text)
                if measure in ["ترابایت", "TB"]:
                    r *= 1024
                return r

        if text != None:
            return text

        return text

    def get_keys(self):
        return {"dynamic": list(self.dynamic_path.keys()),
                "static": list(self.static_path.keys())}

    def get_values(self, max_items, ):
        result = []
        keys = self.get_keys()
        # fetch static keys

        static_values = [self.value_extractor("model"),
                         self.value_extractor("capacity")]
        availabe_shops = len(self.driver.get_elements(self.base_dynamic_path.format(item="*")))
        for item in range(1, min(max_items, availabe_shops) + 1):
            vals = [self.value_extractor(key, item) for key in keys["dynamic"]] + static_values
            for i in vals:
                if type(i) is str and"ناموجود" in i:
                    break
            key_dic = [*keys["dynamic"]] + [*keys["static"]]
            result.append(
                dict(zip(key_dic, vals
                         )))

        return result
