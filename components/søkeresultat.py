from components.film import Film
from components.serie import Serie
from components.fnutt import Fnutt
import requests as req

class Søkeresultat:
    """En klasse som henter data fra OMDb"""
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
        """
        Setter sammen den endelige url-en som skal brukes for å fetche informasjon
        Den avhenger av OMDb key, et søkeord som enten er en tittel eller IMDb-id eller søkemetode
        som bestemmer om man søker med tittel eller id
        """
        if søkemetode == "s":
            return delvis_url + f"?apikey={key}" + f"&s={søkeord}"
        
        elif søkemetode == "id":
            return delvis_url + f"?apikey={key}" + f"&i={søkeord}"
        
        else:
            return False

    @staticmethod
    def _hent_data(url:str) -> dict:
        """Henter data når den endelige url-en er oppgitt (endelig url inkluderer queries deriblant API-key)"""
        resultat = req.get(url)

        if not resultat.status_code == 200:
            print("En feil oppstod når vi prøvde å hente info fra omdbapi.com")
            return None

        data = resultat.json()
        if data["Response"]:
            return data
        
        print("Søket ditt fikk ingen resultater")
        return None
    
    def hent_film(self, søkeord:str, søkemetode:str) -> bool:
        """Selve funksjonen som fetcher svar fra API-en og lagrer dataen i listen hentet_data"""    
        self.url = self.lag_url(self._delvis_url, self.key, søkeord, søkemetode)
        data = self._hent_data(self.url)

        if data['Response'] == 'False': #Sjekker om responsen feilet
            return False
        if søkeord == "id": # Om man søker med ID får man bare 1 svar
            if data["Type"] == "movie":
                fetched_data = Film(data["Title"],data["Released"],data["Ratings"],data["Actors"],data["Genre"],data["Plot"],data["imdbID"],data["Runtime"])
                self._hentet_data.append(fetched_data)
                return True
            elif data["Type"] == "series":
                fetched_data = Serie(data["Title"],data["Released"],data["Ratings"],data["Actors"],data["Genre"],data["Plot"],data["imdbID"],data["totalSeasons"])      
                self._hentet_data.append(fetched_data)
                return True
            else:
                print(f"Unrecognized mediatype: {data['Type']}")
                return False
        
        else: # Her søker man med tittel. Dette gir opp mot 10 svar og gir en udetaljert svar
            for element in data['Search']:
                if element["Type"] == "movie":
                    fetched_data = Fnutt(element["Title"],"movie",element['Year'],element["imdbID"])
                    self._hentet_data.append(fetched_data)
                elif element["Type"] == "series":
                    fetched_data = Fnutt(element["Title"],"series",element['Year'], element["imdbID"])
                    self._hentet_data.append(fetched_data)
                else:
                    print(f"Unrecognized mediatype: {data['Type']}")
            return True