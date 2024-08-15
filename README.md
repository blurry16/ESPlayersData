# ESPlayersData ![](https://img.shields.io/github/last-commit/blurry16/ESPlayersData?path=data%2Fuuids.json&label=new%20player%20to%20ES) ![](https://img.shields.io/github/last-commit/blurry16/ESPlayersData?path=data%2Fes_players_data.json&label=last%20commit%20to%20es_players_data.json)

So this repo was created because ES section in github.com/blurry16/MCDataCollector was looking really weird. Anyways, I
removed comments from there and now this software should work perfectly.  
I coded this thing when I wanted to make a sorted list of Emerald Shores players.  
UUID can be obtained through Mojang API or NameMC. Use whatever you want.
Old versions can be obtained at github.com/blurry16/MCDataCollector commits history.

### How do you add new players to member-list?

So, at least for now you will have to put player's UUID in the uuids.json file.  
Fork the repository, edit the file, and pull request updated version of the file.  
Bot uses the file hosted on GitHub.

### Requirements

Clone the repository and do `pip install -r requirements.txt`.

### main.py args

There are only 2 args in there.gpy

#### -u || --update || --upd </h4>

Updates data and dumps it into file at ESPLAYERSDATAPATH.

#### -c || --commit </h4>

Commits the update at ESPLAYERSDATAPATH. Comment is "es_players_data.json update №X" by default.

#### -nc || --no-cooldown </h4>

Removes cooldown while updating. Works only with --update.

#### -p || --push </h4>

Literally `git push`. Works only with --commit.
