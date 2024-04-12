import json
import requests as req
from components.film import Film
from components.serie import Serie
class Bucketlist:
    def __init__(self, navn_favoritter:dict, url:str, key:str, filplassering:str) -> None:
        self._url = url
        self._key = key
        self._filplassering = filplassering
        self._navn_favoritter = navn_favoritter
        self._favoritter_underholdning = []
    
    @property
    def url(self):
        return self._url
    
    @property
    def key(self):
        return self._key
    
    @property
    def filplassering(self):
        return self._filplassering

    def __str__(self):
        self._oppdater_liste()
        beskrivelse = f"Dette er din liste med favoritt filmer!"
        for i,favoritt in enumerate(self._favoritter_underholdning):
            beskrivelse += f"\nFilm {i+1}!!!"+str(favoritt)
        return beskrivelse
    
    def _oppdater_liste(self):
        for element in self._navn_favoritter["info"]:
            data = self._hent_data(self.url, self.key, element[0])
            if element[1] == "series":
                self._favoritter_underholdning.append(Serie(data["Title"],data["Released"],data["Ratings"],data["Actors"],data["Genre"],data["Plot"],data["imdbID"],data["Runtime"]))
            elif element[1] == "movie":
                self._favoritter_underholdning.append(Film(data["Title"],data["Released"],data["Ratings"],data["Actors"],data["Genre"],data["Plot"],data["imdbID"],data["Runtime"]))

    
    @staticmethod
    def _hent_data(url, key, søkeord):
        resultat = req.get(url + f"?apikey={key}" + f"&t={søkeord}")

        if not resultat.status_code == 200:
            print("En feil oppstod når vi prøvde å hente filminfo fra omdbapi.com")
            return None

        data = resultat.json()
        if data["Response"]:
            return data
        
        print("Søket ditt fikk ingen resultater")
        return None

    @classmethod
    def from_JSON(cls, url:str, key:str, filplassering:str):
        with open(filplassering, "r", encoding="utf-8") as fil:
            data = json.load(fil)
        return cls(data, url, key,filplassering)
    
    def legg_til_favoritt(self, favoritt:str, mediatype:Film|Serie):
        self._navn_favoritter["info"].append([favoritt,mediatype])
    
    def lagre_data(self):
        self._navn_favoritter["info"] = self.fjern_duplikater(self._navn_favoritter["info"])
        with open(self._filplassering, "w") as json_fil:
            json.dump(self._navn_favoritter, json_fil, indent=4)
    
    @staticmethod
    def fjern_duplikater(liste):
        nyliste = []
        for element in liste:
            if not element in nyliste:
                nyliste.append([element[0],element[1]])
        return nyliste