from components.multimedium import Multimedium

class Film(Multimedium):
    def __init__(self, tittel: str, utgivelsesår: int, ratings: list, skuespillere: list, sjanger: list, plot: str, id: int, runtime: int) -> None:
        super().__init__(tittel, utgivelsesår, ratings, skuespillere, sjanger, plot, id)
        self._runtime = runtime
        self.type = "movie"
    
    def __str__(self):
        beskrivelse = f"""
{self._tittel} ({self.utgivelsesår})
ID: {self._id}
Lengde: {self._runtime}
    Ratinger
        IMDb: {self._ratings[0]}
        Rotten Tomatoes: {self.ratings[1]}
        Metacritic: {self.ratings[2]}
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
    def runtime(self):
        return self._runtime