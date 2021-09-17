class ProductLocationResale:
    
    __id = None
    __endereco = None
    __cidade = None
    __cidade_id = None
    __estado = None
    __latitude = None
    __longitude = None
    __regiao_id = None
    
    def __init__(self):
        pass
    
    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id
    
    def get_endereco(self):
        return self.__endereco

    def set_endereco(self, endereco):
        self.__endereco = endereco

    def get_cidade(self):
        return self.__cidade

    def set_cidade(self, cidade):
        self.__cidade = cidade
    
    def get_cidade_id(self):
        return self.__cidade_id

    def set_cidade_id(self, cidade_id):
        self.__cidade_id = cidade_id
    
    def get_estado(self):
        return self.__estado

    def set_estado(self, estado):
        self.__estado = estado

    def get_latitude(self):
        return self.__latitude

    def set_latitude(self, latitude):
        self.__latitude = latitude
    
    def get_longitude(self):
        return self.__longitude

    def set_longitude(self, longitude):
        self.__longitude = longitude

    def get_regiao_id(self):
        return self.__regiao_id

    def set_regiao_id(self, regiao_id):
        self.__regiao_id = regiao_id
    
    def to_string(self):
        return f"[Local] - ID: {self.get_id()} - Endereço: {self.get_endereco()} - Cidade: {self.get_cidade()} - Cidade ID: {self.get_cidade_id()} - Estado: {self.get_estado()} - Latitude: {self.get_latitude()} - Longitude: {self.get_longitude()} - Região ID: {self.get_regiao_id()}"