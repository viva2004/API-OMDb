class Fnutt():
    """En klasse som representerer svarene fra OMDb api som ikke er detaljerte"""
    def __init__(self, tittel, medietype, utgivelsesdato, id) -> None:
        self._tittel = tittel
        self._type = medietype
        self._utgivelsesdato = utgivelsesdato
        self._id = id

    
    def __str__(self) -> str:
        beskrivelse = f"""
{self.tittel} ({self.utgivelsesdato})
ID: {self.id}           
"""
        return beskrivelse
    
    @property
    def tittel(self):
        return self._tittel
    
    @property
    def type(self):
        return self._type
    
    @property
    def utgivelsesdato(self):
        return self._utgivelsesdato
    
    @property
    def id(self):
        return self._id