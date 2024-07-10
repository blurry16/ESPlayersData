from mojang import API
from colorama import Back, Fore, init
from typing import Union
from sys import argv
import os
import requests
import json
import time

ESPLAYERSDATAPATH = r"C:\Development\Python3\ESPlayersData\es_players_data.json"


class Jsonfile:
    """yes. well i just like how it works i'm too lasy to do with open() blocks lol"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> Union[dict, list]:
        """loads data from json file"""
        with open(self.file_path, "r", encoding="UTF-8") as data_file:
            return json.load(data_file)

    def dump(self, data: Union[dict, list], indent=4):
        """dumps selected data to the file"""
        with open(self.file_path, "w", encoding="UTF-8") as data_file:
            json.dump(data, data_file, indent=indent)


esplayersdata = Jsonfile(ESPLAYERSDATAPATH)
uuids = json.loads(
    requests.get(
        "https://raw.githubusercontent.com/blurry16/ESPlayersData/main/uuids.json"
    ).text
)


argv = [i.lower() for i in argv]

if __name__ == "__main__":

    init(autoreset=True)

    mapi = API()
    data = esplayersdata.load()
    if "--update" in argv or "--upd" in argv:
        print(Fore.RESET)
        length = len(uuids)
        for index, i in enumerate(uuids):
            profile = mapi.get_profile(i)
            data[profile.id] = {
                "id": profile.id,
                "name": profile.name,
                "is_legacy_profile": profile.is_legacy_profile,
                "skin_variant": profile.skin_variant,
                "cape_url": profile.cape_url,
                "skin_url": profile.skin_url,
            }
            print(f"{Fore.GREEN}{profile.name} updated. [{index + 1}/{length}]")
            print(json.dumps(data[profile.id], indent=2))
            print("\n")
            time.sleep(1)
        del length
        esplayersdata.dump(data)
        print(f"{Back.GREEN}Successfully dumped data in {esplayersdata.file_path}")
    data = esplayersdata.load()
    if "--push" in argv:
        os.system(
            f'cd {os.curdir} && git add {ESPLAYERSDATAPATH} && git commit -m "es_players_data.json update" && git push'
        )
    names = [data[i]["name"] for i in data]
    uuids_upd_dict = {data[i]["name"]: data[i]["id"] for i in data}
    print(json.dumps(data, indent=2))
    print("\n".join(sorted(names)))
    print(names, end="\n" * 2)
    print(uuids_upd_dict, end="\n" * 2)
    print(len(names), len(data), len(uuids), end="\n\n")
    for name in uuids_upd_dict:
        print(f"{uuids_upd_dict[name]}: {name}")
