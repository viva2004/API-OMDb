class Multimedium:
    """
    En klasse som lagrer på informasjonen som mottas fra OMDb. 
    Denne klassen er også foreldreklasse for film og serie
    """
    def __init__(self,tittel:str, utgivelsesår: int, ratings: list, skuespillere: str, sjanger: str, plot: str, id: int) -> None:
        self._tittel = tittel
        self._utgivelsesår = utgivelsesår
        self._ratings = ratings
        self._skuespillere = skuespillere.split(",")
        self._sjanger = sjanger.split(",")
        self._plot = plot
        self._id = id
    
    @property
    def tittel(self):
        return self._tittel
    
    @property
    def utgivelsesår(self):
        return self._utgivelsesår
    
    @property
    def ratings(self):
        return self._ratings
    
    @property
    def skuespillere(self):
        return self._skuespillere
    
    @property
    def sjanger(self):
        return self._sjanger
    
    @property
    def plot(self):
        return self._plot
    
    @property
    def id(self):
        return self._id