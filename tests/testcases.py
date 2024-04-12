import data.settings
import os
from components.søkeresultat import Søkeresultat
from components.bucket_list import Bucketlist
def testcases_søkeresultat():
    mine_søk = Søkeresultat(data.settings.API_URL, data.settings.API_KEY)
    mine_søk.hent_film("Star Wars", "t")
    assert (
        mine_søk._hentet_data[0].id == "tt0076759"
    ), f"Det er noe galt med søkefunksjonen. ID den hentet er {mine_søk._hentet_data[0].id} når det skulle vært tt0076759"


def testcases_bucketlist():
    filplassering = os.path.join(
        os.path.abspath(os.path.dirname("__file__")), r"data\test_data.json"
    )
    bucket_list = Bucketlist.from_JSON(
        data.settings.API_URL,
        data.settings.API_KEY,
        filplassering,
    )
    bucket_list.legg_til_favoritt("Justified", "series")
    assert bucket_list._navn_favoritter["info"][0] == [
        "Justified",
        "series",
    ], f"Feil tolkning av riktig syntakse i legg til funksjonen. Det ble: {bucket_list._navn_favoritter['info'][0]} istedenfor: {['Justified', 'series']}"
    bucket_list.legg_til_favoritt("Star Wars", "movie")
    bucket_list.lagre_data()
