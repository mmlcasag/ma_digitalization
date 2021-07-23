import requests

from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, page_url):
        self.__page_url = page_url
        self.__page_number = 1
        self.__page_html = self.__crawl()

    def __crawl(self):
        webpage = requests.get(self.__page_url)
        return BeautifulSoup(webpage.content, "html.parser")

    def get_page_url(self):
        return self.__page_url

    def get_page_number(self):
        return self.__page_number

    def get_page(self):
        return self.__page_html

    def get_parent_category(self):
        return self.__page_html.select("div.vertical-menu a.catParent")

    def get_categories(self):
        return self.__page_html.select("div.vertical-menu a.catChild")

    def get_subcategories(self):
        return self.__page_html.select("div.vertical-menu a.catGrandChild")

    def get_products(self):
        return self.__page_html.find_all("div", attrs={"class": "element"})

    def get_products_url(self):
        urls = []
        for element in self.__page_html.find_all("div", attrs={"class": "element"}):
            id = ""
            for char in element["onclick"]:
                if char.isdigit():
                    id = id + char
            urls.append(f"https://vendas.queirozgalvao.com/?p={id}")
        return urls

    def get_next_page(self):
        html_next_page = self.__page_html.find("div", attrs={"class": "nav-next"})

        try:
            page_url = html_next_page.find("a")

            self.__page_url = page_url["href"]
            self.__page_number = self.__page_number + 1
            self.__page_html = self.__crawl()
        except Exception:
            self.__page_url = ""
            self.__page_number = 0
            self.__page_html = ""

    def has_next_page(self):
        html_next_page = self.__page_html.find("div", attrs={"class": "nav-next"})

        if html_next_page.find_all("a") > 0:
            return True

        return False
