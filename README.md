# ESPlayersData
So this repo was created because ES section in github.com/blurry16/MCDataCollector was looking really weird. Anyways, I removed comments from there and now this software should work perfectly.  
I coded this thing when I wanted to make a sorted list of Emerald Shores players.  
To add a new player you just need to add their nickname and uuid in "uuids" dictionary. It should look somehow like this: `"NAME": "UUID"`.  
UUID can be obtained through Mojang API or NameMC. Use whatever you want.
Old versions can be obtained at github.com/blurry16/MCDataCollector commits history.  
Feel free to pull request updated `es_players_data.json` files and lists/dictionaries inside `get_nicknames_es.py`.

### Requirements
Just clone the repository and do `pip install -r requirements.txt`.  
