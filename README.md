A chatbot for Telegram.


What can it do?
===============

Tell you stories written in [ink](https://github.com/inkle/ink).
Send `/start` and answer its prompts.


Where to test it?
=================

You can add Iria on Telegram at [`@iria_bot`](http://t.me/iria_bot).

Though, as it should be understood, I take no responsability
for interruptions of service or loss of data due to testing,
feature upgrades, sysadmin troubles or basically any reason!

If you want stability, deploy your own version 😊


How to deploy?
==============

1. Register with [the BotFather](https://core.telegram.org/bots) so you get your bot token.
2. Clone this repo.
3. Place the bot token into a new file `app/secrets/token.json`:
```
{"token": "YOUR-BOT-TOKEN-STRING"}
```
4. Run `make install` the first time to get dependencies.
5. Replace `app/ink/game.ink` with your own story if you like, and then run `make json`.
6. Run `make start` et voilà!
    * To keep it running forever with `pm2`, you can use `make launch` instead.

Iria is MIT licensed, so you can do pretty much whatever you want as long
as you include the original copyright and license notice in any copy of the code.
Experiment, have fun, and drop me a notice if you make something cool based on her.


Why the name?
=============

Iria has been so many things throughout the years! A Jabber bot, a Telegram bot…
It has told jokes, made dictionary lookups, searched for gifs…
it even organised RPG games at one point!

Nowadays Iria tells stories, and therefore it could be the acronym for `Iria Relata Intrincadas Aventuras`,
but decades ago it was born as an IRC bot and stood for `IRC Intelixencia Artificial`,
as well as being a nice Galician name—and it has kept it all along.


Attribution
===========

Based on [ink-telegram](https://github.com/technix/ink-telegram) by Serhii "techniX" Mozhaiskyi, (c) 2019.
