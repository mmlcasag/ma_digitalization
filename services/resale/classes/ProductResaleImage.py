class ProductResaleImage:
    
    __id = None
    __nome = None
    __mimetype = None
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

    def get_mimetype(self):
        return self.__mimetype

    def set_mimetype(self, mimetype):
        self.__mimetype = mimetype
    
    def get_url(self):
        return self.__url

    def set_url(self, url):
        self.__url = url
    
    def to_string(self):
        return f"[Imagem] - ID: {self.get_id()} - Nome: {self.get_nome()} - MimeType: {self.get_mimetype()} - URL: {self.get_url()}"