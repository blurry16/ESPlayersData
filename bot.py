# Imports
import json
import time
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
MEMBERLISTID: int = 0  # ID of the member list channel
MEMBERLISTMESSAGEID: int = 0  # ID of the member list message
ROLEID: int = 0  # ID of the role with permission to force updates

argv = [arg.lower() for arg in argv]  # Formatting the CLI args

init(autoreset=True)  # Initializing colorama (colorama.init)

bot = commands.Bot(
    command_prefix="..",
    intents=disnake.Intents.all(),
    status=disnake.Status.offline,
)  # Initializing Discord bot, giving it command prefix, intents and status.

mapi = mojang.API()  # Initializing mojang API

updates = 0  # Initializing update counter


@bot.event
async def on_ready() -> None:
    """Discord bot on-ready event. Is caused by bot start."""
    print(f"{Fore.MAGENTA}Bot {bot.user} is ready!")  # Logging
    update_task.start()  # Starting the update task to update in-discord member list.


@bot.slash_command(description="Force an update.", dm_permission=False)
async def update(inter: disnake.ApplicationCommandInteraction) -> None:
    """/update | Simply forces a member list update.
    """
    if inter.author.get_role(ROLEID):  # Checking permission
        try:
            print(f"{Fore.MAGENTA}{inter.author} forced an update at {int(time.time())}.")  # Logging
            await inter.send("Update was forced successfully!", ephemeral=True)
            await update_data()
        except disnake.errors.InteractionTimedOut:  # If an update is already going, it will cause time out
            print(f"{Fore.RED}{inter.author} timed out trying to update at {int(time.time())}.")  # Logging
    else:
        await inter.send("Not enough permissions.", ephemeral=True)


async def update_data() -> None:
    """
    Function that updates data. Is used in the update task and by /update commnad.
    """
    try:
        global updates  # Globalising updates counter variable
        uuids = json.loads(requests.get(JSONRAWURL).text)  # Loading uuids via JSON hosted somewhere (GitHub)
        await (bot.get_channel(COUNTCHANNELID)
               .edit(name=f"{len(uuids)} players in ES"))  # Editing channel name to the actual number of players
        await bot.get_channel(MEMBERLISTID).get_partial_message(
            MEMBERLISTMESSAGEID
        ).edit(content=f"{len(uuids)} players in ES\n"
                       f"Updating... Started <t:{int(time.time())}:R> (<t:{int(time.time())}:f>)\n" +
                       ("100 reached on 1st September 2024 :tada:\n" if "--no-stats" not in argv else "") +
                       f"[GitHub repo](https://github.com/blurry16/ESPlayersData)"
               )  # Editing the main member list message to a placeholder
        names = []  # Initializing a local list of names
        for index, uuid in enumerate(uuids):  # Iterating through uuids and getting nickname via UUID
            username = mapi.get_username(uuid)  # Sending request via Mojang API to get an actual name of a player
            names.append(username)  # Appending the username to the list
            print(f"[{index + 1}/{len(uuids)}] {uuid} -> {Fore.GREEN}{username}")  # Logging
        del username, index, uuid  # Sending useless variables to the hell
        tojoin = "\n".join(sorted(names))  # String that was created to be joinedf
        content = (f"{len(uuids)} players in ES\n```\n{tojoin}\n```\nUpdated <t:{int(time.time())}:R>"
                   f" (<t:{int(time.time())}:f>)\n" +
                   ("100 reached on 1st September 2024 :tada:\n" if "--no-stats" not in argv else "") +
                   f"[GitHub repo](https://github.com/blurry16/ESPlayersData)"
                   )  # Whole content of the member list message
        await bot.get_channel(MEMBERLISTID).get_partial_message(
            MEMBERLISTMESSAGEID
        ).edit(
            content=content
        )  # Editing the member list message with the content
        updates += 1  # Increasing the update counter
        print(f"\n{content}\n")  # Logging
        if "-c" in argv or "--copy" in argv:  # checking if the content should be copied the clipboard
            clipboard.copy(content)  # copying the content to the clipboard
            print(f"{Fore.GREEN}The content was successfully copied to your clipboard.")  # Logging
        print(
            f"{Fore.GREEN}Data successfully updated at {int(time.time())}. "
            f"In sum {updates} update{'s' if updates > 1 else ''} ha{'ve' if updates > 1 else 's'} taken place."
        )  # Logging
    except Exception as e:
        print(f"{Fore.RED}Exception {e} occurred.")  # logging


@tasks.loop(minutes=15)
async def update_task() -> None:
    """the main task aka update task"""
    await update_data()  # lol


if __name__ == "__main__":
    bot.run(TOKEN)  # running the bot if the file is not imported
