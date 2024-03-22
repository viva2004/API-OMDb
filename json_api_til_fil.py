import data.settings
import requests
import json

def hent_film_info(tittel):
    """ Hente informasjon om et film"""
    #Konfigurerer kall til API
    api_key = data.settings.API_KEY  # Du må erstatte 'din_omdb_api_nøkkel' med din egen 
    url = f'http://www.omdbapi.com/?apikey={api_key}&t={tittel}'  #test her forskjellige kall
    
    #Kalle tjeneste fra API og hente resultater.
    response = requests.get(url)
    if response.status_code == 200:  # sjekker at HTTP request til API gikk bra.
        film_data = response.json()
        if film_data["Response"] == "False":   #sjekker om OMDb API tjeneste kall gikk bra.
            print(film_data["Error"])
            return None
        return film_data
    else:
        print('Feil ved henting av filminformasjon.')
        return None

def lagre_film_info(data, filename):
    """ Lagre informasjon om et film"""
    with open(filename, 'w') as json_fil:
        json.dump(data, json_fil, indent=4)

if __name__ == '__main__':
    film_tittel = input('Skriv inn tittelen på filmen: ')
    film_info = hent_film_info(film_tittel)
    if film_info:
        filnavn = f'film_info.json'
        lagre_film_info(film_info, filnavn)
        print(f'Filminformasjonen er lagret i "{filnavn}" filen.')
