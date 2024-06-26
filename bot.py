import disnake
import requests
import json
import time
import mojang
from colorama import init, Fore
from disnake.ext import commands, tasks

TOKEN = ""
JSONRAWURL = "https://raw.githubusercontent.com/blurry16/ESPlayersData/main/uuids.json"
COUNTCHANNELID = 1254552599210885274
MEMBERLISTID = 1254554188461903882
MEMBERLISTMESSAGEID = 1254556785386328136
ROLEID = 1254744804110241822

init(autoreset=True)

bot = commands.Bot(
    command_prefix="..",
    intents=disnake.Intents.all(),
    status=disnake.Status.offline,
)

mapi = mojang.API()

updates = 0


@bot.event
async def on_ready():
    print(f"{Fore.MAGENTA}Bot {bot.user} is ready!")
    update_task.start()


@bot.slash_command(description="Force an update.", dm_permission=False)
async def update(ctx):
    if ctx.author.get_role(ROLEID):
        print(f"{Fore.MAGENTA}{ctx.author} forced an update at {int(time.time())}.")
        await ctx.send("Update was forced successfully!", ephemeral=True)
        await update_data()
    else:
        await ctx.send("Not enough permissions.", ephemeral=True)


async def update_data():
    try:
        global updates
        uuids = json.loads(requests.get(JSONRAWURL).text)
        await bot.get_channel(COUNTCHANNELID).edit(name=f"{len(uuids)} players in ES")
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


if __name__ == "__main__":
    bot.run(TOKEN)
