# This repo is archived due to the end of CV7.
Emerald Shores was a great project, and I'm thrilled that I was involved in it. 
Thanks to everybody who has contributed to it.  
This repository was my small contribution, simple sorted member list. Good luck and see you again, nubs!

# ESPlayersData ![](https://img.shields.io/github/last-commit/blurry16/ESPlayersData?path=data%2Fuuids.json&label=new%20player%20to%20ES) ![](https://img.shields.io/github/last-commit/blurry16/ESPlayersData?path=data%2Fes_players_data.json&label=last%20commit%20to%20es_players_data.json)

So this repo was created because ES section
in [github.com/blurry16/MCDataCollector](https://github.com/blurry16/MCDataCollector) was looking really weird. Anyways,
I
removed comments from there and now this software should work perfectly.  
I coded this thing when I wanted to make a sorted list of Emerald Shores players.  
UUID can be obtained through Mojang API or NameMC. Use whatever you want.
Old versions can be obtained at [github.com/blurry16/MCDataCollector](https://github.com/blurry16/MCDataCollector)
commits history.

### How do you add new players to member-list?

So, at least for now you will have to put player's UUID in
the [uuids.json](https://github.com/blurry16/ESPlayersData/blob/main/data/uuids.json) file.  
Fork the repository, edit the file, and pull request updated version of the file.  
Bot uses the file hosted on GitHub.

### Requirements

Clone the repository and do `pip install -r requirements.txt`.

### main.py args

#### -u || --update || --upd

Updates data and dumps it into file at ESPLAYERSDATAPATH.

#### -p || --push

Commits and push updated data on GitHub.

#### -nc || --no-cooldown

Removes cooldown while updating. Works only with --update.

### bot.py args

#### -cc || --copy

Copies updated content to your clipboard.
It was added since it may be annoying to always get your clipboard cleared while doing other stuff.

#### --no-stats

Removes stats lines.