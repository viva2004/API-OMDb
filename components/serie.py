from components.multimedium import Multimedium

class Serie(Multimedium):
    """En klasse som representerer en film utifra OMDb informasjon"""
    def __init__(self, tittel: str, utgivelsesår: int, ratings: list, skuespillere: list, sjanger: list, plot: str, id: int, antall_sesonger: int) -> None:
        super().__init__(tittel, utgivelsesår, ratings, skuespillere, sjanger, plot, id)
        self._antall_sesonger = antall_sesonger
        self.type = "series"

    
    def __str__(self):
        beskrivelse = f"""
{self._tittel} ({self.utgivelsesår})
ID: {self._id}
Sesonger: {self.antall_sesonger}
    Ratinger"""
        for rating in self.ratings:
            beskrivelse += f"""
        {rating["Source"]}: {rating["Value"]}"""
        beskrivelse += f"""
    Skuespillere
        {self._skuespillere[0]}
        {self._skuespillere[1]}
        {self._skuespillere[2]}
    Sjanger
        {self._sjanger[0]}
        {self._sjanger[1]}
        {self._sjanger[2]}
    Synopsis
        {self._plot}
"""
        return beskrivelse

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
    
    @property
    def antall_sesonger(self):
        return self._antall_sesonger