class Fnutt():
    def __init__(self, tittel, medietype, utgivelsesdato, id) -> None:
        self.tittel = tittel
        self.type = medietype
        self.utgivelsesdato = utgivelsesdato
        self.id = id

    
    def __str__(self) -> str:
        beskrivelse = f"""
{self.tittel} ({self.utgivelsesdato})
ID: {self.id}           
"""
        return beskrivelse