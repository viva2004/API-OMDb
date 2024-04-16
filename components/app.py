import data.settings
from components.søkeresultat import Søkeresultat
from components.bucket_list import Bucketlist

class App:
    """Klasse som kjører og enkapsulerer funksjonaliteten til ARGS-flix"""
    def __init__(self) -> None:
        self.søkeresultat = Søkeresultat(data.settings.API_URL, data.settings.API_KEY)
        self.bucket_list_filplassering = r"data\bucket_list.json"
        self.bucket_list = Bucketlist.from_JSON(
            data.settings.API_URL,
            data.settings.API_KEY,
            self.bucket_list_filplassering,
        )

    def _velkommen(self) -> str:
        """Lager velkomsten til bruker ved oppstart"""
        velkomst = f"""
Hei! Velkommen til din OMDb app. 
Denne tekstbaserte appen tilbyr muligheten til å søke på film og serier
og lagre dine favoritter. 

Foreløpig er din liste med favoritter:
{self.bucket_list._data_favoritter["favoritter"]}
"""
        return velkomst

    def _vis_grensesnitt(self) -> str:
        """Lager utskrift av hvilke valg brukeren kan ta"""
        grensesnitt = f"""
################################################
Hovedside
_________
Skriv inn bokstaven ved siden av funksjonen du vil anvende
    1. Se detaljert bucketlist 'd'  2. Legg søkte elementer i bucketlist 'l'
    
    3. Fjern fra bucketlist 'f'     4. Søk på film 's'

    5. Marker som sett 'm'          6. Exit 'e'

"""
        return grensesnitt

    def _hent_søkeresultat(self):
        """Samler all den praktiske koden/front enden som brukeren skal interagere med når de velger å søke"""
        søkemetode = input("Skriv s/ID om du vil søke etter tittel/ID\n- ")
        if not søkemetode.lower() in ["s", "id"]:   # Sørger for at brukeren velger å enten søke som tittel eller id
            while not søkemetode.lower() in ["s", "id"]:
                print("Søkemetode må enten være 's' eller 'id'")
                søkemetode = input("Skriv s/ID om du vil søke etter tittel/ID\n- ")

        if søkemetode == "s":   # Forskjellig utskrift avhengig av metoden man søker på filmer
            søkeord = input("Skriv inn tittelen på filmen du ser etter:\n")
        else:
            søkeord = input("Skriv inn ID på filmen du ser etter:\n")

        return self.søkeresultat.hent_film(søkeord, søkemetode) # Lagrer hentet_data i søkeresultat

    def _legg_til(self):
        """
        Metode for om brukeren velger 'l' som legger til data fra søkeresultatene i bucketlist.
        Kan bare kjøres om brukeren allerede har søkeresultater.
        """
        if len(self.søkeresultat._hentet_data) == 0:    # Sjekker om bruker har noen søkeresultater
            print("Du har ikke søkt på en film som du kan legge til ennå")
            return None
        print(f"Dine søkte elementer hittil er:")
        for i,søk in enumerate(self.søkeresultat._hentet_data):
            print(f"Søk {i+1}:{søk}")
        while True: # Henter index til søkeresultatet som skal lagres i bucketlist
            try:
                søknmr = int(input("Skriv hvilken nmr i søkelisten din filmen du vil lagre ligger i\n- "))
                if not (0 < søknmr <= len(self.søkeresultat._hentet_data)):
                    print("Det fins ikke et element med det nummeret")
                    continue
                søknmr -= 1
                break
            except ValueError:
                print("Vennligst skriv et tall og ikke noe mer")
        self.bucket_list.legg_til_favoritt(self.søkeresultat._hentet_data[søknmr].tittel, self.søkeresultat._hentet_data[søknmr].type)
        print(f"Din bucket list består nå av:\n {self.bucket_list._data_favoritter['favoritter']}")

    def _fjern(self):
        """
        Fjerner en film eller serie fra bucketlist. 
        Inneholder frontend som ikke befinner seg i bucketlist metoden
        """
        sett_eller_favoritt = input("Vil du fjerne en favoritt fra bucketlist eller en film du har sett\nSkriv fav/sett\n- ").lower()
        sjekk_sett_eller_favoritt = ["fav","sett"]  # Liste med tillate tast fra brukerens side 
        while not sett_eller_favoritt in sjekk_sett_eller_favoritt: # SØrger for at input er 'sett' eller 'fav'
            sett_eller_favoritt = input("Skriv 'fav' for favoritt eller 'sett' for å avmerke en sett film\n- ")
        if sett_eller_favoritt == 'sett':
            if len(self.bucket_list._data_favoritter['sett']) == 0: # Kan ikke fjerne fra sett-listen om ingen er markert fra før
                print('Du har ikke markert noen filmer som sett')
                return None
            print(f"Dette er filmene du har sett:\n{self.bucket_list._data_favoritter['sett']}")
            while True: # Sjekker at bruker taster inn en gyldig index
                try:
                    element_plassering = int(input("Hvilken nummer i listen er elementet du vil fjerne?\n- "))-1
                    if not (0 < element_plassering+1 <= len(self.bucket_list._data_favoritter['sett'])):
                        print("Gitt indeks finnes ikke i listen")
                        continue
                    break
                except ValueError:
                    print("Skriv bare tall og ikke annet. Det du svarer skal kunne konverteres til et tall")
            print(f'Fjernet elementet {self.bucket_list.fjern_film(sett_eller_favoritt,element_plassering)}')
        elif sett_eller_favoritt == 'fav':
            print(f'Foreløpig er din liste med favoritter:\n{self.bucket_list._data_favoritter["favoritter"]}')
            film_fjern = input("Skriv inn navnet på filmen du vil fjerne\n- ")
            # Sjekker om tittelen brukeren tastet inn befinner seg i bucketlist
            for i,favoritt in enumerate(self.bucket_list._data_favoritter["favoritter"]):  
                if film_fjern.lower() == favoritt[0].lower():
                    print(f'Fjernet elementet {self.bucket_list.fjern_film("favoritter",i)}')
                    return None
            print(f'Det var ingen elementer i listen med tittelen {film_fjern}')
            
            

        

    def kjør(self):
        """Kjører appen. Den eneste koden brukeren skal kjøre"""
        print(self._velkommen())
        tillate_tast = ['d','l','f','s','e','m']
        while True: # App loop
            print(self._vis_grensesnitt())
            bruker_gjøremål = input("Skriv enten d/l/f/s/m for å benytte deg av våre tjenester eller 'e' for å exitte\n- ")
            if not bruker_gjøremål.lower() in tillate_tast: # Sørger for at bruker svarer noe som er tillat
                while not bruker_gjøremål.lower() in tillate_tast:
                    bruker_gjøremål = input("Prøv på nytt. Inputten var ikke et av følgende d/l/f/s/m/e\n- ")
            match bruker_gjøremål.lower():
                case "d":   # Detaljert bucketlist
                    print(self.bucket_list)
                case "l":   # Legg til
                    self._legg_til()
                case "f":   # Fjern element fra favoritt eller sett
                    self._fjern()
                case "s":   # Søk på OMDb
                    if self._hent_søkeresultat():   # True om søket er en suksess
                        print(f"Dine søkte elementer hittil er:")
                        for i,søk in enumerate(self.søkeresultat._hentet_data):
                            print(f"Søk {i+1}:{søk}")
                    else:
                        print("Invalid search")
                case "m":   # Marker som sett
                    id_sett = input("Skriv ID-en til filmen som du har sett\n- ")
                    tittel = self.bucket_list.marker_sett(id_sett)  # Henter tittel til film som ble markert og lagrer markerte elementer
                    if not tittel == None:
                        print(f"La til filmen {tittel}")
                    else:
                        print("Det fins ingen filmer med den IMDb ID-en")
                case "e":   # Exit app
                    print("Ha det!")
                    self.bucket_list.lagre_data()
                    break
        print("Filmene venter her til neste gang!")
