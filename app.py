import data.settings
import requests as req
import json


def hent_film(temp_url: str, key: str, søkeord: str):
    url = temp_url + f"?apikey={key}" + f"&t={søkeord}"
    resultat = req.get(url)

    if not resultat.status_code == 200:
        print("En feil oppstod når vi prøvde å hente filminfo fra omdbapi.com")
        return None

    data = resultat.json()
    if data["Resoponse"]:
        return data
    print("Søket ditt fikk ingen resultater")
    return None


def lagre_data(data, filename):
    with open(filename, "w") as json_fil:
        json.dump(data, json_fil, indent=4)


def main():
    print(hent_film(data.settings.API_URL, data.settings.API_KEY, "star wars"))


if __name__ == "__main__":
    main()
