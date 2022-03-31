import json

from app import models


def dump_countries(file_path="app/utils/countries.json") -> bool:
    try:
        with open(file_path, "r") as file_ins:
            countries_data = json.loads(file_ins.read())
            for country in countries_data:
                models.Country.objects.get_or_create(
                    name=country["name"],
                    code=country["code"]
                )
            return True
    except:
        return False
