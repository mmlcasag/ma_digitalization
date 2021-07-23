class Category:
    def __init__(self, html):
        self.html = html
        self.__id = self.__scrape_id()
        self.__name = self.__scrape_name()
        self.__type = self.__scrape_type()
        self.__url = self.__scrape_url()
        self.__product_count = self.__scrape_product_count()
        self.__products = []

    def __scrape_id(self):
        try:
            id = ""
            for char in self.html["href"]:
                if char.isdigit():
                    id = id + char
            id = int(id)
        except Exception:
            id = 0
        finally:
            return id

    def __scrape_name(self):
        try:
            name = self.html.string[0 : self.html.string.index("(")]
        except Exception:
            name = ""
        finally:
            return name

    def __scrape_type(self):
        try:
            type = self.html["class"]
            if "catParent" in type:
                type = "All"
            if "catChild" in type:
                type = "Category"
            if "catGrandChild" in type:
                type = "Subcategory"
        except Exception:
            type = ""
        finally:
            return type

    def __scrape_url(self):
        try:
            url = self.html["href"]
        except Exception:
            url = ""
        finally:
            return url

    def __scrape_product_count(self):
        try:
            product_count = int(
                self.html.string[
                    self.html.string.index("(") + 1 : self.html.string.index(")")
                ]
            )
        except Exception:
            product_count = 0
        finally:
            return product_count

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_url(self):
        return self.__url

    def get_product_count(self):
        return self.__product_count

    def get_products(self):
        return self.__products

    def get_total_products(self):
        return len(self.__products)

    def get_full_description(self):
        return "Mais informações sobre a categoria: <br>ID: {}<br>Nome: {}<br>Tipo: {}<br>URL: {}<br>Qtd. de Produtos: {}".format(
            self.get_id(),
            self.get_name(),
            self.get_type(),
            self.get_url(),
            self.get_product_count(),
        )

    def to_string(self):
        return "Categoria: ID: {} - Nome: {} - Tipo: {} - URL: {} - Qtd. de Produtos: {}".format(
            self.get_id(),
            self.get_name(),
            self.get_type(),
            self.get_url(),
            self.get_product_count(),
        )

    def add_product(self, product):
        self.__products.append(product)
