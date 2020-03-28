A chatbot for Telegram.


What can it do?
===============

It helps you play Fate Accelerated through Telegram (work in progress).

* `/roll sequence` rolls dice. `sequence` takes the usual RPG pattern, i.e. `3d6+1d10+7`.
This is basically a copy of the code from the great
[Roll'em Bot](https://github.com/treetrnk/rollem-telegram-bot).
Check the license in the link.
* `/roll`, with no argument, rolls `4dF` by default (four Fate dice)

It also has two Easter Eggs commands:

* `/g tag` or `/gifsapm tag` posts a random APM gif taken
from the [APM Gifs tumblr](http://gifsapm.tumblr.com)
based on the tag passed.
* `/e word` or `/estraviz word` searches for that word
in the [Estraviz dictionary](http://estraviz.org).


Where to test it?
=================

You can add Iria on Telegram at [`@iria_bot`](http://t.me/iria_bot).

Though, as it should be understood, I take no responsability
for interruptions of service or loss of data due to testing,
feature upgrades, sysadmin troubles or basically any reason!

If you want stability, deploy your own version 😊


How to deploy?
==============

1. Clone the repo in a machine that has Docker.
2. Register with [the BotFather](https://core.telegram.org/bots)
so you get your own token. Place it into `data/secret/bot_token`.
3. Run `docker-compose up -d` et voilà!

Iria is MIT licensed, so you can do pretty much whatever you want as long
as you include the original copyright and license notice in any copy of the code.
Experiment, have fun, and drop me a notice if you make something cool based on her.

Note that for the APM gifs easter egg to work,
you need a `data/secret/tumblr_token` containing the Tumblr tokens for
- consumer key
- consumer secret
- access token
- access secret

in consecutive, different lines. (In its absence the plugin is just not loaded).



Why the name?
=============

Way, way back it used to be an IRC bot (see that messy first commit).
So IRIA stood for `IRC Intelixencia Artificial`, as well as being a nice Galician name.
I then ported it to Jabber, before finally porting it to Telegram, but kept the name as I liked it.

It could now be backronymed into `"It's not my fault, Really!" IA`.
