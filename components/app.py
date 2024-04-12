import data.settings
import os
from components.søkeresultat import Søkeresultat
from components.bucket_list import Bucketlist


class App:
    def __init__(self) -> None:
        self.søkeresultat = Søkeresultat(data.settings.API_URL, data.settings.API_KEY)
        self.bucket_list_filplassering = os.path.join(
            os.path.abspath(os.path.dirname("__file__")), r"data\bucket_list.json"
        )
        self.bucket_list = Bucketlist.from_JSON(
            data.settings.API_URL,
            data.settings.API_KEY,
            self.bucket_list_filplassering,
        )

    def _hent_søkeresultat(self):
        søkemetode = input("Skriv t/ID om du vil søke etter tittel/ID")
        if not søkemetode.lower() in ["t", "id"]:
            while not søkemetode.lower() in ["t", "id"]:
                print("Søkemetode må enten være 't' eller 'id'")
                søkemetode = input("Skriv t/ID om du vil søke etter tittel/ID")

        if søkemetode == "t":
            søkeord = input("Skriv inn tittelen på filmen du ser etter:\n")
        else:
            søkeord = input("Skriv inn ID på filmen du ser etter:\n")

        self.søkeresultat.hent_film(søkeord, søkemetode)

    def _velkommen(self):
        velkomst = f"""
Hei! Velkommen til din OMDb app. 
Denne tekstbaserte appen tilbyr muligheten til å søke på film og serier
og lagre dine favoritter. 

Foreløpig er din liste med favoritter:
{self.bucket_list._navn_favoritter["info"]}
"""
        return velkomst

    def _vis_grensesnitt(self):
        grensesnitt = f"""
################################################
Hovedside
_________
Skriv inn bokstaven ved siden av funksjonen du vil anvende
    1. Se detaljert bucketlist 'd'  2. Legg søkte elementer i bucketlist 'l'
    
    3. Fjern fra bucketlist 'f'     4. Søk på film 's'

    5. Exit 'e'

"""
        return grensesnitt

    def _legg_til(self):
        if len(self.søkeresultat._hentet_data) == 0:
            print("Du har ikke søkt på en film som du kan legge til ennå")
            return None
        print(f"Dine søkte elementer hittil er:")
        for i,søk in enumerate(self.søkeresultat._hentet_data):
            print(f"Søk {i+1}:{søk}")
        while True:
            try:
                søknmr = int(input("Skriv hvilken nmr i søkelisten din filmen du vil lagre ligger i"))
                if 0 >= søknmr > len(self.søkeresultat._hentet_data):
                    print("Det fins ikke et element med det nummeret")
                    continue
                søknmr -= 1
                break
            except ValueError:
                print("Vennligst skriv et tall og ikke noe mer")
        self.bucket_list.legg_til_favoritt(self.søkeresultat._hentet_data[søknmr].tittel, self.søkeresultat._hentet_data[søknmr].type)
        print(f"Din bucket list består nå av:\n {self.bucket_list._navn_favoritter['info']}")

    def kjør(self):
        print(self._velkommen())
        while True:
            print(self._vis_grensesnitt())
            bruker_gjøremål = input("Skriv enten d/l/f/s for å benytte deg av våre tjenester eller 'e' for å exitte\n")
            if not bruker_gjøremål.lower() in ['d','l','f','s','e']:
                while not bruker_gjøremål.lower() in ['d','l','f','s','e']:
                    bruker_gjøremål = input("Prøv på nytt. Inputten var ikke et av følgende d/l/f/s/e")
            match bruker_gjøremål.lower():
                case "d":
                    print(self.bucket_list)
                case "l":
                    self._legg_til()
                case "f":
                    pass
                case "s":
                    self._hent_søkeresultat()
                    print(f"Dine søkte elementer hittil er:")
                    for i,søk in enumerate(self.søkeresultat._hentet_data):
                        print(f"Søk {i+1}:{søk}")
                case "e":
                    print("Ha det!")
                    self.bucket_list.lagre_data()
                    break
        print("Filmene venter her til neste gang!")
