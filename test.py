class multimedium:
    def __init__(self, id = None, tittel = None) -> None:
        if tittel == None and id ==None:
            print("Feilmelding, trenger enten tittel eller id")
        
        elif tittel != None and id != None:
            print("Bare tittel eller id helst")
        
        elif tittel != None:
            self.tittel = tittel
            self.hent_data_tittel(tittel = tittel)
        
        elif id != None:
            self.tittel = tittel
            self.hent_data_ID(tittel = tittel)
    
    def hent_data_ID(self, ID):
        return None
    
    def hent_data_tittel(self, tittel):
        return None

