# ESPlayersData
So this repo was created because ES section in github.com/blurry16/MCDataCollector was looking really weird. Anyways, I removed comments from there and now this software should work perfectly.  
I coded this thing when I wanted to make a sorted list of Emerald Shores players.  
UUID can be obtained through Mojang API or NameMC. Use whatever you want.
Old versions can be obtained at github.com/blurry16/MCDataCollector commits history.  

### How do you add new players to member-list?
So, at least for now you will have to put player's UUID in the uuids.json file.  
Fork the repository, edit the file, and pull request updated version of the file.  
Bot uses the file that is hosted on GitHub.

### Requirements
Just clone the repository and do `pip install -r requirements.txt`.  

## main.py argv
There are only 2 argv in there:

#### --update || --upd
Updates data and dumps it into file at ESPLAYERSDATAPATH.

#### --push
Pushes the file update at ESPLAYERSDATAPATH on GitHub. Comment is "es_players_data.json update" by default.

#### --bot || --discord || --discord-bot
Runs the Discord bot after --update and --push (if they were even launched).