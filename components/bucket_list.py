import json
from typing import Self
import requests as req
from components.film import Film
from components.serie import Serie
class Bucketlist:
    """Lager en bucketlist som kan lagre på dine favoritt filmer og hvilke filmer du har sett i en JSON fil"""
    def __init__(self, data_favoritter:dict, url:str, key:str, filplassering:str) -> None:
        self._url = url
        self._key = key
        self._filplassering = filplassering
        self._data_favoritter = data_favoritter
        self._detaljert_favoritter = []
    
    @classmethod
    def from_JSON(cls, url:str, key:str, filplassering:str) -> Self:
        """
        Tillater opprettelsen av bucketlist om man oppgir en JSON-fil

            Parametre:
                cls : Det samme som self. Referer til klassen selv
                url : URL til API-en uten noen ekstra informasjon fra queries
                key : API-KEY som man bruker for å aksessere OMDb
                filplassering : Stedet hvor filen er lagret på datamaskinen
            
            Retur:
                En instanse av Bucketlist laget av informasjonen som ligger i JSON-filen referert til
        """
        with open(filplassering, "r", encoding="utf-8") as fil:
            try:
                data = json.load(fil)
            except json.JSONDecodeError: # Error som oppstår når JSON-filen ikke engang inneholder et objekt
                data = {}
            if len(data) == 0:
                data = {"favoritter":[], "sett":[]}
        return cls(data, url, key,filplassering)
    
    @property
    def url(self):
        return self._url
    
    @property
    def key(self):
        return self._key
    
    @property
    def filplassering(self):
        return self._filplassering

    def __str__(self) -> str:
        self._oppdater_liste()
        beskrivelse = f"Dette er din liste med favoritt medieelementer!"
        for i,favoritt in enumerate(self._detaljert_favoritter):    # Itererer gjennom favorittene
            if favoritt.tittel in self._data_favoritter["sett"]:        # Sjekker om tittelen er markert som sett
                beskrivelse += "\nFølgende element har du sett"
            else:
                beskrivelse += "\nFølgende element har du ikke sett"
            beskrivelse += f"\nElement {i+1}!!!"+str(favoritt)
        
        beskrivelse += "\nDisse har du allerede sett:\n"    # Viser en oversikt over filmene du har sett
        for i,favoritt in enumerate(self._data_favoritter["sett"]):
            beskrivelse += f"{favoritt} "
        return beskrivelse
    
    def _oppdater_liste(self):
        """Sørger for å fjerne duplikater i favoritter og 'sett'-listen og henter detaljerte versjoner av favorittene"""
        self._data_favoritter["sett"] = list(set(self._data_favoritter["sett"]))
        self._data_favoritter["favoritter"] = self.fjern_duplikater(self._data_favoritter["favoritter"])
        self._detaljert_favoritter = []     # Lager detaljert data på nytt hver gang funksjonen kjøres
        for element in self._data_favoritter["favoritter"]:
            data = self._hent_data(self.url, self.key, element[0])
            if element[1] == "series":
                self._detaljert_favoritter.append(Serie(data["Title"],data["Released"],data["Ratings"],data["Actors"],data["Genre"],data["Plot"],data["imdbID"],data["Runtime"]))
            elif element[1] == "movie":
                self._detaljert_favoritter.append(Film(data["Title"],data["Released"],data["Ratings"],data["Actors"],data["Genre"],data["Plot"],data["imdbID"],data["Runtime"]))
        
    @staticmethod
    def _hent_data(url:str, key:str, søkeord:str) -> dict:
        """Hjelpefunksjon for å hente data"""
        resultat = req.get(url + f"?apikey={key}" + f"&t={søkeord}")

        if not resultat.status_code == 200:
            print("En feil oppstod når vi prøvde å hente filminfo fra omdbapi.com")
            return None

        data = resultat.json()
        if data["Response"] == 'True':  # Må sette True som streng fordi bools ikke konverteres fra str når funksjonen .json() brukes
            return data
        
        print("Søket ditt fikk ingen resultater")
        return None
    
    def legg_til_favoritt(self, favoritt:str, mediatype:Film|Serie) -> None:
        """
        Oppgi navn og medietype for å lagre en favoritt i bucketlist.
        Lagres i formen [tittel, mediatype] i attributten Bucketlist.data_favoritter. 
        Eks: ['Justified', 'series']
        """
        self._data_favoritter["favoritter"].append([favoritt,mediatype])
        self._oppdater_liste()

    def fjern_film(self,hva:str,element:int) -> list:
        """Brukes for å fjerne film gitt index i favoritt-listen"""
        fjernet_element = self._data_favoritter[hva].pop(element)
        self._oppdater_liste()
        return fjernet_element

    
    def marker_sett(self, id:str) -> str:
        """Markerer en fil som sett om du oppgir en id"""
        resultat = req.get(self.url + f"?apikey={self.key}" + f"&i={id}")
        data = resultat.json()
        if data["Response"] == 'True':
            self._data_favoritter["sett"].append(data["Title"])
            self._oppdater_liste()
            return data['Title']
    
        return False
        
        
    
    def lagre_data(self):
        """
        Metode som lagrer data i filplasseringen som er lagret i klassen som JSON. 
        Overskriver alt som sto i JSON-filen fra før av med den oppdaterte bucketlisten
        """
        self._data_favoritter["favoritter"] = self.fjern_duplikater(self._data_favoritter["favoritter"])
        with open(self._filplassering, "w") as json_fil:
            json.dump(self._data_favoritter, json_fil, indent=4)
    
    @staticmethod
    def fjern_duplikater(liste:list) -> list:
        """
        Hjelpefunksjon som fjerner duplikater av favoritt dataen med den spesifikke syntaksen den har
        Et eksempel på dette er [["Justified","series"], ["Justified","series"]] -> ["Justified","series"]
        """
        nyliste = []
        for element in liste:
            if not element in nyliste:
                nyliste.append([element[0],element[1]])
        return nyliste