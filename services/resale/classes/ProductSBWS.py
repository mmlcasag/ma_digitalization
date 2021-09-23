class ProductSBWS:
    
    __productId = None
    __productYourRef = None
    __externalId = None
    __shortDesc = None
    __detailedDesc = None
    __status = None
    __statusId = None
    __statusDesc = None
    __sellerId = None
    __productTypeId = None
    __parentCategoryId = None
    __categoryId = None
    __subCategoryId = None
    __partnerIntegrationId = None
    __createdAt = None
    __locationId = None
    __placeId = None
    __cityId = None
    __latitude = None
    __longitude = None
    __eventManagerId = None
    __hasPhotoAttachment = None
    __photoIllustrative = None
    __hasOffers = None
    __hasActiveOffer = None
    __activeOfferId = None
    __pendingStatus = None
    __pendingStatusDesc = None
    __inConditions = None
    
    def __init__(self):
        pass

    def get_productId(self):
        return self.__productId

    def set_productId(self, productId):
        self.__productId = productId
    
    def get_productYourRef(self):
        return self.__productYourRef

    def set_productYourRef(self, productYourRef):
        self.__productYourRef = productYourRef
    
    def get_externalId(self):
        return self.__externalId

    def set_externalId(self, externalId):
        self.__externalId = externalId
    
    def get_shortDesc(self):
        return self.__shortDesc

    def set_shortDesc(self, shortDesc):
        self.__shortDesc = shortDesc
    
    def get_detailedDesc(self):
        return self.__detailedDesc

    def set_detailedDesc(self, detailedDesc):
        self.__detailedDesc = detailedDesc
    
    def get_status(self):
        return self.__status
    
    def set_status(self, status):
        self.__status = status
    
    def get_statusId(self):
        return self.__statusId

    def set_statusId(self, statusId):
        self.__statusId = statusId
    
    def get_statusDesc(self):
        return self.__statusDesc

    def set_statusDesc(self, statusDesc):
        self.__statusDesc = statusDesc

    def get_sellerId(self):
        return self.__sellerId

    def set_sellerId(self, sellerId):
        self.__sellerId = sellerId

    def get_productTypeId(self):
        return self.__productTypeId

    def set_productTypeId(self, productTypeId):
        self.__productTypeId = productTypeId
    
    def get_parentCategoryId(self):
        return self.__parentCategoryId

    def set_parentCategoryId(self, parentCategoryId):
        self.__parentCategoryId = parentCategoryId
    
    def get_categoryId(self):
        return self.__categoryId

    def set_categoryId(self, categoryId):
        self.__categoryId = categoryId
    
    def get_subCategoryId(self):
        return self.__subCategoryId

    def set_subCategoryId(self, subCategoryId):
        self.__subCategoryId = subCategoryId
    
    def get_partnerIntegrationId(self):
        return self.__partnerIntegrationId

    def set_partnerIntegrationId(self, partnerIntegrationId):
        self.__partnerIntegrationId = partnerIntegrationId
    
    def get_createdAt(self):
        return self.__createdAt

    def set_createdAt(self, createdAt):
        self.__createdAt = createdAt
    
    def get_locationId(self):
        return self.__locationId

    def set_locationId(self, locationId):
        self.__locationId = locationId
    
    def get_placeId(self):
        return self.__placeId

    def set_placeId(self, placeId):
        self.__placeId = placeId
    
    def get_cityId(self):
        return self.__cityId

    def set_cityId(self, cityId):
        self.__cityId = cityId
    
    def get_latitude(self):
        return self.__latitude

    def set_latitude(self, latitude):
        self.__latitude = latitude
    
    def get_longitude(self):
        return self.__longitude

    def set_longitude(self, longitude):
        self.__longitude = longitude
    
    def get_eventManagerId(self):
        return self.__eventManagerId

    def set_eventManagerId(self, eventManagerId):
        self.__eventManagerId = eventManagerId
    
    def get_hasPhotoAttachment(self):
        return self.__hasPhotoAttachment

    def set_hasPhotoAttachment(self, hasPhotoAttachment):
        self.__hasPhotoAttachment = hasPhotoAttachment
    
    def get_photoIllustrative(self):
        return self.__photoIllustrative

    def set_photoIllustrative(self, photoIllustrative):
        self.__photoIllustrative = photoIllustrative
    
    def get_hasOffers(self):
        return self.__hasOffers
    
    def set_hasOffers(self, hasOffers):
        self.__hasOffers = hasOffers

    def get_hasActiveOffer(self):
        return self.__hasActiveOffer
    
    def set_hasActiveOffer(self, hasActiveOffer):
        self.__hasActiveOffer = hasActiveOffer

    def get_activeOfferId(self):
        return self.__activeOfferId
    
    def set_activeOfferId(self, activeOfferId):
        self.__activeOfferId = activeOfferId
    
    def get_pendingStatus(self):
        return self.__pendingStatus
    
    def set_pendingStatus(self, pendingStatus):
        self.__pendingStatus = pendingStatus
    
    def get_pendingStatusDesc(self):
        return self.__pendingStatusDesc
    
    def set_pendingStatusDesc(self, pendingStatusDesc):
        self.__pendingStatusDesc = pendingStatusDesc
    
    def get_inConditions(self):
        return self.__inConditions
    
    def set_inConditions(self, inConditions):
        self.__inConditions = inConditions
    
    def to_string(self):
        return f"[Produto SBWS] - productId: {self.get_productId()} - productYourRef: {self.get_productYourRef()} - externalId: {self.get_externalId()} - shortDesc: {self.get_shortDesc()} - detailedDesc: {self.get_detailedDesc()} - statusId: {self.get_statusId()} - statusDesc: {self.get_statusDesc()} - productTypeId: {self.get_productTypeId()} - parentCategoryId: {self.get_parentCategoryId()} - categoryId: {self.get_categoryId()} - subCategoryId: {self.get_subCategoryId()} - partnerIntegrationId: {self.get_partnerIntegrationId()} - createdAt: {self.get_createdAt()} - locationId: {self.get_locationId()} - placeId: {self.get_placeId()} - cityId: {self.get_cityId()} - latitude: {self.get_latitude()} - longitude: {self.get_longitude()} - eventManagerId: {self.get_eventManagerId()} - hasPhotoAttachment: {self.get_hasPhotoAttachment()} - photoIllustrative: {self.get_photoIllustrative()} - hasOffers: {self.get_hasOffers()} - hasActiveOffer: {self.get_hasActiveOffer()} - activeOfferId: {self.get_activeOfferId()} - pendingStatus: {self.get_pendingStatus()} - pendingStatusDesc: {self.get_pendingStatusDesc()} - inConditions: {self.get_inConditions()}"