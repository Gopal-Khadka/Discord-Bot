import requests


class Country:
    def __init__(self, name: str, type, url_var):
        self.name = name
        self.type = type
        self.var = url_var
        self.message = self.country_info()

    def country_info(self):
        api_url = f"https://restcountries.com/v3.1/{self.var}/{self.name.lower()}"
        try:
            response = requests.get(api_url).json()[0]
        except KeyError:
            return f"Given query {self.name} maybe incorrect or not a {self.type}!!!"
        else:
            self.o_name = response["name"].get("official")
            self.capital = response["capital"][0]
            langs_list = [value for key, value in response["languages"].items()]
            self.langs = ",".join(langs_list)
            self.flag = response["flags"].get("png")
            self.icon = response["flag"]
            self.area = response["area"]
            self.population = response["population"]
            self.continent = response["continents"][0]
            time_zone = response["timezones"]
            self.time_zones = " , ".join(time_zone)
            message = f"""
        User Query: {self.name}
        The official name of the country is {self.o_name}
        Capital city: {self.capital}
        Spoken Languages: {self.langs}
        Flag: {self.icon}
        Flag Image: {self.flag}
        Area: {self.area} square metres
        Population: {self.population}
        Continent: {self.continent}
        Time zones:{self.time_zones}
        """
            return message
