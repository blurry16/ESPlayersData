# Imports
import json
import os
import time
from pathlib import Path
from sys import argv

import requests
from colorama import Back, Fore, init
from mojang import API

# Paths
ESPLAYERSDATAPATH = Path(r"data/es_players_data.json")
COMMITCOUNTERPATH = Path("data/es_players_data_commit_counter.txt")

# URLs
UUIDSURL = "https://raw.githubusercontent.com/blurry16/ESPlayersData/main/data/uuids.json"
ESPLAYERSDATAGITHUBURL = "https://raw.githubusercontent.com/blurry16/ESPlayersData/main/data/es_players_data.json"
COMMITCOUNTERURL = "https://raw.githubusercontent.com/blurry16/ESPlayersData/main/data/es_players_data_commit_counter.txt"


class JsonFile:
    """JsonFile class contains required methods to work with .json files"""

    def __init__(self, file_path: Path | str) -> None:
        self.file_path: Path = Path(file_path)

    def load(self) -> dict | list:
        """loads data from json file"""
        with open(self.file_path, "r", encoding="UTF-8") as data_file:
            return json.load(data_file)

    def dump(self, data: dict | list, indent: int = 2) -> None:
        """dumps selected data to the file"""
        with open(self.file_path, "w", encoding="UTF-8") as data_file:
            json.dump(data, data_file, indent=indent)


# I believe that JsonFile class is already understandable, since it's written as simple as possible >.<


esplayersdata = JsonFile(ESPLAYERSDATAPATH)  # Init main jsonfile object
uuids = json.loads(requests.get(UUIDSURL).text)  # get uuid via get request

argv = [i.lower() for i in argv]  # Format args

if __name__ == "__main__":

    init(autoreset=True)  # Init colorama

    mapi = API()  # Init Mojang API
    data = esplayersdata.load()  # load data

    if "--update" in argv or "--upd" in argv or "-u" in argv:  # update section
        length = len(uuids)
        for index, i in enumerate(uuids):  # iterating through uuids and getting profiles
            profile = mapi.get_profile(i)
            data[profile.id] = {
                "id": profile.id,
                "name": profile.name,
                "skin_variant": profile.skin_variant,
                "cape_url": profile.cape_url,
                "skin_url": profile.skin_url,
            }

            # Logging
            print(f"{Fore.GREEN}{profile.name} updated. [{index + 1}/{length}]")
            print(json.dumps(data[profile.id], indent=2))
            print("\n")

            time.sleep(0 if "--no-cooldown" in argv or "-nc" in argv else 0.25)  # sleep if no arg given
        del length
        esplayersdata.dump(data)  # dump data
        print(f"{Back.GREEN}Successfully dumped data in {esplayersdata.file_path}")  # logging
    data: dict = esplayersdata.load()  # load data. again
    names = [data[i]["name"] for i in data]  # get names only
    uuids_upd_dict = {data[i]["name"]: data[i]["id"] for i in data}  # get 'name: uuid' dict

    # Logging
    print(json.dumps(data, indent=2))
    print("\n".join(sorted(names)))
    print(names, end="\n" * 2)
    print(uuids_upd_dict, end="\n" * 2)
    print(len(names), len(data), len(uuids), end="\n\n")
    for name in uuids_upd_dict:
        print(f"{uuids_upd_dict[name]}: {name}")
    print()

    githubdata: dict = json.loads(requests.get(ESPLAYERSDATAGITHUBURL).text)  # get data from github
    if "--push" not in argv and "-p" not in argv and data != githubdata:  # no push & data updated section
        print(f"{Fore.GREEN}Data was updated. It's ready to be pushed!")

    elif ("--push" in argv or "-p" in argv) and data != githubdata:  # push section & data updated

        # count commit (just simply +1 to what's written in file)
        with open(COMMITCOUNTERPATH, "r") as file:
            count = int(file.read())
        with open(COMMITCOUNTERPATH, "w") as file:
            file.write(str(count + 1))

        # Git commands
        os.system(
            f'cd {os.curdir} '
            f'&& git add {ESPLAYERSDATAPATH} '
            f'&& git add {COMMITCOUNTERPATH} '
            f'&& git commit -m "es_players_data.json update №{open(COMMITCOUNTERPATH, "r").read()}" '
            f'&& git push'
        )
    else:  # Data not updated section or (not updated | push)
        print(f"{Fore.RED}The data on GitHub is already up to date.")

    # Logging
    print(f"\nBy GitHub RAW file, {Fore.GREEN + requests.get(url=COMMITCOUNTERURL).text + Fore.RESET} "
          f"updates of es_players_data.json have taken place.")
    print(f"By local file, {Fore.GREEN + open(COMMITCOUNTERPATH, 'r').read() + Fore.RESET} "
          f"updates of es_players_data.json have taken place.")
