class ProductFileResale:
    
    __id = None
    __nome = None
    __tipo = None
    __url = None
    
    def __init__(self):
        pass
    
    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id
    
    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        self.__nome = nome

    def get_tipo(self):
        return self.__tipo

    def set_tipo(self, tipo):
        self.__tipo = tipo
    
    def get_url(self):
        return self.__url

    def set_url(self, url):
        self.__url = url
    
    def to_string(self):
        return f"""
            ID: {self.get_id()}\n
            Nome: {self.get_nome()}\n
            Tipo: {self.get_tipo()}\n
            URL: {self.get_url()}\n
        """