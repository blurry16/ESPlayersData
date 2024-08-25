import json
import time
import typing
from sys import argv

import clipboard
import disnake
import mojang
import requests
from colorama import init, Fore
from disnake.ext import commands, tasks

TOKEN: str = ""  # Discord bot token
JSONRAWURL: str = "https://raw.githubusercontent.com/blurry16/ESPlayersData/main/data/uuids.json"  # UUIDs list RAW url
COUNTCHANNELID: int = 0  # ID of "X players in ES" channel
MEMBERLISTID: int = 0  # ID of member list channel
MEMBERLISTMESSAGEID: int = 0  # ID of member list message
ROLEID: int = 0  # ID of the role with permission to force updates

argv = [arg.lower() for arg in argv]

init(autoreset=True)

bot = commands.Bot(
    command_prefix="..",
    intents=disnake.Intents.all(),
    status=disnake.Status.offline,
)

mapi = mojang.API()

updates = 0


@bot.event
async def on_ready() -> None:
    print(f"{Fore.MAGENTA}Bot {bot.user} is ready!")
    update_task.start()


@bot.slash_command(description="Force an update.", dm_permission=False)
async def update(inter: disnake.ApplicationCommandInteraction) -> None:
    if inter.author.get_role(ROLEID):
        try:
            print(f"{Fore.MAGENTA}{inter.author} forced an update at {int(time.time())}.")
            await inter.send("Update was forced successfully!", ephemeral=True)
            await update_data()
        except disnake.errors.InteractionTimedOut:
            print(f"{Fore.RED}{inter.author} timed out trying to update {int(time.time())}.")
    else:
        await inter.send("Not enough permissions.", ephemeral=True)


async def async_iter(iterable: typing.Iterable) -> typing.Generator[typing.Any, None, None]:
    for index, i in enumerate(iterable):
        yield index, i


async def update_data() -> None:
    try:
        global updates
        uuids = json.loads(requests.get(JSONRAWURL).text)
        await bot.get_channel(COUNTCHANNELID).edit(name=f"{len(uuids)} players in ES")
        names = []
        async for index, uuid in async_iter(uuids):
            username = mapi.get_username(uuid)
            names.append(username)
            print(f"[{index + 1}/{len(uuids)}] {uuid} -> {Fore.GREEN}{username}")
        del username, index, uuid
        tojoin = "\n".join(sorted(names))
        content = (f"{len(uuids)} players\n```\n{tojoin}\n```\nUpdated <t:{int(time.time())}:R>"
                   f" (<t:{int(time.time())}:f>)\n"
                   f"[GitHub repo](https://github.com/blurry16/ESPlayersData)")
        await bot.get_channel(MEMBERLISTID).get_partial_message(
            MEMBERLISTMESSAGEID
        ).edit(
            content=content
        )
        updates += 1
        print(f"\n{content}\n")
        if "-c" in argv or "--copy" in argv:
            clipboard.copy(content)
            print(f"{Fore.GREEN}The content was successfully copied to your clipboard.")
        print(
            f"{Fore.GREEN}Data successfully updated at {int(time.time())}. "
            f"In sum {updates} update{'s' if updates > 1 else ''} ha{'ve' if updates > 1 else 's'} taken place."
        )
    except Exception as e:
        print(f"{Fore.RED}Exception {e} occurred.")


@tasks.loop(minutes=15)
async def update_task() -> None:
    await update_data()


if __name__ == "__main__":
    bot.run(TOKEN)
