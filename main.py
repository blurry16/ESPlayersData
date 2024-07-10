from mojang import API
from colorama import Back, Fore, init
from typing import Union
from sys import argv
from disnake.ext import commands, tasks
import disnake
import requests
import json
import time
import os


ESPLAYERSDATAPATH = r"C:\Development\Python3\ESPlayersData\es_players_data.json"

TOKEN = ""
JSONRAWURL = "https://raw.githubusercontent.com/blurry16/ESPlayersData/main/uuids.json"
COUNTCHANNELID = 1254552599210885274
MEMBERLISTID = 1254554188461903882
MEMBERLISTMESSAGEID = 1254556785386328136
ROLEID = 1254744804110241822


class Jsonfile:
    """yes. well i just like how it works i'm too lasy to do with open() blocks lol"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> Union[dict, list]:
        """loads data from json file"""
        with open(self.file_path, "r", encoding="UTF-8") as data_file:
            return json.load(data_file)

    def dump(self, _data: Union[dict, list], indent=4):
        """dumps selected data to the file"""
        with open(self.file_path, "w", encoding="UTF-8") as data_file:
            json.dump(_data, data_file, indent=indent)


updates = 0


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
    olddata = esplayersdata.load()
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
    names = [data[i]["name"] for i in data]
    uuids_upd_dict = {data[i]["name"]: data[i]["id"] for i in data}
    print(json.dumps(data, indent=2))
    print("\n".join(sorted(names)))
    print(names, end="\n" * 2)
    print(uuids_upd_dict, end="\n" * 2)
    print(len(names), len(data), len(uuids), end="\n\n")
    for name in uuids_upd_dict:
        print(f"{uuids_upd_dict[name]}: {name}")
    if "--push" not in argv and data != olddata:
        print(f"{Fore.GREEN}Data was updated. It's ready to be pushed!")

    if "--push" in argv:
        os.system(
            f'cd {os.curdir} && git add {ESPLAYERSDATAPATH} && git commit -m "es_players_data.json update" && git push'
        )

    if "--bot" in argv or "--discord" in argv or "--discord-bot" in argv:
        activity = disnake.Activity(
            name="check bio",
            type=disnake.ActivityType.playing,
        )
        bot = commands.Bot(
            command_prefix="..",
            intents=disnake.Intents.all(),
            status=disnake.Status.online,
            activity=activity,
        )

        @bot.event
        async def on_ready():
            print(f"{Fore.MAGENTA}Bot {bot.user} is ready!")
            update_task.start()

        @bot.slash_command(description="Force an update.", dm_permission=False)
        async def update(ctx):
            if ctx.author.get_role(ROLEID):
                print(
                    f"{Fore.MAGENTA}{ctx.author} forced an update at {int(time.time())}."
                )
                await ctx.send("Update was forced successfully!", ephemeral=True)
                await update_data()
            else:
                await ctx.send("Not enough permissions.", ephemeral=True)

        async def update_data():
            try:
                global updates
                uuids = json.loads(requests.get(JSONRAWURL).text)
                await bot.get_channel(COUNTCHANNELID).edit(
                    name=f"{len(uuids)} players in ES"
                )
                names = [mapi.get_username(i) for i in uuids]
                tojoin = "\n".join(sorted(names))
                await bot.get_channel(MEMBERLISTID).get_partial_message(
                    MEMBERLISTMESSAGEID
                ).edit(
                    content=f"```\n{tojoin}\n```\nUpdated <t:{int(time.time())}:R> (<t:{int(time.time())}:f>)\n[GitHub repo](https://github.com/blurry16/ESPlayersData)"
                )
                updates += 1
                print(
                    f"{Fore.GREEN}Data successfully updated at {int(time.time())}. In sum {updates} update{'s' if updates > 1 else ''} ha{'ve' if updates > 1 else 's'} taken place."
                )
            except Exception as e:
                print(f"{Fore.RED}Exception {e} occurred.")

        @tasks.loop(minutes=15)
        async def update_task():
            await update_data()

        bot.run(TOKEN)
