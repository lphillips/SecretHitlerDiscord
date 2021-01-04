# SecretHitlerDiscord
This is a Discord bot for the famous game Secret Hitler. Secret Hitler is a game like werewolf or mafia. Every player gets a secret role: Liberal, Fascist or Hitler. The fascists know each other and try to install their cold-blooded leader. The liberals try to find and stop the secret hitler before it's too late.

You need 5-10 players to play this game. You can see the rules here: [Click here for the rules!](https://cdn.vapid.site/sites/a67e0c72-4902-4365-a899-3386df73c2c4/assets/Secret_Hitler_Rules-023bc755617986cb2276a3b6920e43e0.pdf)

This code implements the game in a discord bot, so you can play this game in discord!

Note that this project is still in development. There will be more features and bugfixes soon.

This discord bot is made in Python using pillow and discord.py

## Installation

### Development Environment
Ensure the following tools and libraries are installed.

1. Install Python 3.5 or higher (https://www.python.org/downloads/)
2. Install `git`. `git` is likely already installed on Unix or macOS, but you can get the latest command line `git` at https://git-scm.com/downloads. If you prefer a GUI, https://desktop.github.com/ is GitHub's GUI client, and there are many other GUI wrappers around `git`.
3. Install `pillow` and `discord.py` via
 ```
 pip3 install pillow && pip3 install discord.py
 ```

### Create a Discord application
You will need to create an application and bot on Discord at https://discord.com/developers/applications/ in order to generate an OAuth2 token for the SecretHitler app to send messages to the Discord API.

1. Open https://discord.com/developers/applications/ in a browser and click "New Application".
2. Click on the tile for your new application and optionally add an icon and description under the "General Information" section.
3. Open the "Bot" section and click "Add Bot". For development, disable "Public Bot" so that only you can add your bot to a server. Otherwise, anyone with the bot link can add it to a server.
4. To generate a link to invite the bot to a server, go to the OAuth2 section and click "Bot" under "Scopes". This opens a "Bot Permissions" panel. Enable "Administrator" under "Bot Permissions" and copy the URL in the "Scopes" section.
5. Paste the copied link into the browser address bar and go through the bot invitation flow. The bot is now invited to your server.

### Start SecretHitlerDiscord
The application must be running for the Discord bot to be able to respond to commands from users in Discord. First, you must set up the code to use the OAuth2 token generated when you created the application on Discord's developer site.

Open `main.py`, and scroll to the bottom to find this line:
```
client.run('TOKEN')
```

Replace `TOKEN` with your OAuth2 token, copied from the "Bot" section on your application's page on the Discord developer portal.

![Discord developer portal screenshot](docs/img/discord_bot_oauth2.png)

Click the "Copy" button to copy the token to the clipboard and replace the text "TOKEN" with the copied token string.

```
// TODO: Update these docs with how to set up the token as an environment variable as part of https://github.com/lphillips/SecretHitlerDiscord/issues/8.
```

Start the server by running:
```
python3 main.py
```

## Start game

To start a game use -startgame private <number of players>. A new game channel will be created. Execute -invite <playername> to add a player to this game. After all players joined the game will start.

## Discord API Documentation
https://discordpy.readthedocs.io/en/latest/index.html

## Credits and License

This project is licensed under Creative Commons BY-NC-SA 4.0. You are free to adapt and share the game in any form or format under following conditions. You have to credit us if you use this game. You are not allowed to use the game for commercial use. You have to use the same license as we do (CC BY-NC-SA 4.0). You are not allowed to restrict others from doing anything our license allows. That means you can't submit the app to an app store without approval.

Secret Hitler was created by Mike Boxleiter, Tommy Maranges, Max Temkin, and Mac Schubert (see secrethitler.com). The graphics used for this project are from secrethitlerfree.de and made by Flatimalsstudios. The code used for this game is made by Nergon and also licensed under CC BY-NC-SA 4.0

## Alterations to the original game
I modified the images and slightly adjusted the rules for a better online use.
