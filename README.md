A chatbot for Telegram.


Where to test it?
=================

You can add Iria on Telegram at [`@iria_bot`](http://t.me/iria_bot).


What can it do?
===============

It currently supports three commands:

* `/a tag` posts a random APM gif taken from the [APM Gifs tumblr](http://gifsapm.tumblr.com) based on the tag passed.
* `/e word` searches for that word in the [Estraviz dictionary](http://estraviz.org)
* `/d sequence` rolls dice. `sequence` takes the usual RPG pattern, i.e. `3d6+1d10+7`


Deploy notes
============

Iria is MIT licensed, so you can do pretty much whatever you want as long as you include the original copyright and license notice in any copy of the code.

If you want to deploy your own, you'll need a `secret/bot_token` file with the Telegram token and a `secret/tumblr_token` with the Tumblr tokens for consumer key, consumer secret, access token and access secret in consecutive, different lines.


Why the name?
=============

Way, way back it used to be an IRC bot (see that messy first commit). So Iria stands for IRC Intelixencia Artificial, as well as being a nice Galician name. I then ported it to Jabber, before finally porting it to Telegram, but kept the name as I liked it.