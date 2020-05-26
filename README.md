# SecretHitlerDiscord
This is a discord bot for the famous game SecretHitler. SecretHitler is a game like werewolf or mafia. Every player gets a secret role: Liberal, Fascist or Hitler. The fascists know each other and try to install their cold-blooded leader. The liberals try to find and stop the secret hitler before it's too late.

You need 5-10 players to play this game. You can see the rules here: [Click here for the rules!](https://cdn.vapid.site/sites/a67e0c72-4902-4365-a899-3386df73c2c4/assets/Secret_Hitler_Rules-023bc755617986cb2276a3b6920e43e0.pdf)

This code implements the game in a discord bot, so you can play this game in discord! 

Note that this project is still in development. There will be more features and bugfixes soon.

This discord bot is made in Python using pillow and discord.py

## Installation

### Install your instance
To prevent errors i recommend installing your own instance of the bot.

Install at least python3.5 on your computer/server
Install pip3
Install git
Install pillow and discord.py (pip3 install pillow && pip3 install discord.py)
Create a discord application and copy your token [Click here](https://discord.com/developers/applications/)

then

```
git clone https://github.com/Nergon/SecretHitlerDiscord.git
cd SecretHitlerDiscord
```
now open main.py and scroll down to the end of the file. Replace 'Token' with your discord bot token

then 

```
python3 main.py
```

after a short while the bot will go online. Now invite it to your server and execute -setup

## Start game

to start a game use -startgame private <number of players>. A new game channel will be created. Execute -invite <playername> to add a player to this game. After all players joined the game will start.


## Credits and License

This project is licensed under Creative Commons BY-NC-SA 4.0. You are free to adapt and share the game in any form or format under following conditions. You have to credit us if you use this game. You are not allowed to use the game for commercial use. You have to use the same license as we do (CC BY-NC-SA 4.0). You are not allowed to restrict others from doing anything our license allows. That means you can't submit the app to an app store without approval. 

Secret Hitler was created by Mike Boxleiter, Tommy Maranges, Max Temkin, and Mac Schubert (see secrethitler.com). The graphics used for this project are from secrethitlerfree.de and made by Flatimalsstudios. The code used for this game is made by Nergon and also licensed under CC BY-NC-SA 4.0

## Alterations to the original game
I modified the images and slightly adjusted the rules for a better online use. 
