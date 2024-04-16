import data.settings
import json
from components.søkeresultat import Søkeresultat
from components.bucket_list import Bucketlist


def testcases_søkeresultat():
    mine_søk = Søkeresultat(data.settings.API_URL, data.settings.API_KEY)
    assert mine_søk.lag_url(data.settings.API_URL,data.settings.API_KEY, "tt0094747", "id") == "http://www.omdbapi.com/?apikey=d952421a&i=tt0094747", f'Feil konstruksjon av url. Det skulle vært "http://www.omdbapi.com/?apikey=d952421a&i=tt0094747" men var istedenfor {mine_søk.lag_url(data.settings.API_URL,data.settings.API_KEY, "tt0094747", "id")}'
    mine_søk.hent_film("Star Wars", "s")
    assert (
        mine_søk._hentet_data[0].id == "tt0076759"
    ), f"Det er noe galt med søkefunksjonen. ID den hentet er {mine_søk._hentet_data[0].id} når det skulle vært tt0076759"


def testcases_bucketlist():
    filplassering = r"data\test_data.json"
    with open(filplassering, "w") as json_fil:  # Sørger for at test_data.json er tom på oppstart
            json.dump({}, json_fil, indent=4)
    bucket_list = Bucketlist.from_JSON(
        data.settings.API_URL,
        data.settings.API_KEY,
        filplassering,
    )
    assert bucket_list._data_favoritter == {"favoritter":[], "sett":[]}, f"Default layout av json objekt er ikke rett. Det var {bucket_list._data_favoritter} istedenfor" + r'{"favoritter":[], "sett":[]}'
    bucket_list.legg_til_favoritt("Justified", "series")
    assert bucket_list._data_favoritter["favoritter"][0] == [
        "Justified",
        "series",
    ], f"Feil tolkning av riktig syntakse i legg til funksjonen. Det ble: {bucket_list._data_favoritter['favoritter'][0]} istedenfor: {['Justified', 'series']}"
    bucket_list.legg_til_favoritt("Star Wars", "movie")
    bucket_list.lagre_data()
    bucket_list2 = Bucketlist.from_JSON(
        data.settings.API_URL,
        data.settings.API_KEY,
        filplassering,
    )
    assert bucket_list2._data_favoritter["favoritter"] == [["Justified", "series"],["Star Wars", "movie"],], "Lagrer ikke data etter å ha brukt metoden lagre_data"
