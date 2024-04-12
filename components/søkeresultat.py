from components.film import Film
from components.serie import Serie
import requests as req

class Søkeresultat:
    def __init__(self, url:str, key:str) -> None:
        self._delvis_url = url
        self._key = key
        self.url = None
        self._hentet_data = []

    @property
    def delvis_url(self):
        return self._delvis_url

    @property
    def key(self):
        return self._key
    
    @staticmethod
    def lag_url(delvis_url: str, key: str, søkeord: str, søkemetode = str) -> str:
        if søkemetode == "t":
            return delvis_url + f"?apikey={key}" + f"&t={søkeord}"
        
        elif søkemetode == "id":
            return delvis_url + f"?apikey={key}" + f"&i={søkeord}"
        
        else:
            return False
            

    @staticmethod
    def _hent_data(url):
        resultat = req.get(url)

        if not resultat.status_code == 200:
            print("En feil oppstod når vi prøvde å hente info fra omdbapi.com")
            return None

        data = resultat.json()
        if data["Response"]:
            return data
        
        print("Søket ditt fikk ingen resultater")
        return None
    
    def hent_film(self, søkeord, søkemetode):    
        self.url = self.lag_url(self._delvis_url, self.key, søkeord, søkemetode)
        data = self._hent_data(self.url)
        if data["Type"] == "movie":
            fetched_data = Film(data["Title"],data["Released"],data["Ratings"],data["Actors"],data["Genre"],data["Plot"],data["imdbID"],data["Runtime"])
        elif data["Type"] == "series":
            fetched_data = Serie(data["Title"],data["Released"],data["Ratings"],data["Actors"],data["Genre"],data["Plot"],data["imdbID"],data["totalSeasons"])      
        else:
            print(f"Unrecognized mediatype: {data['Type']}")
            return None
        
        self._hentet_data.append(fetched_data)
