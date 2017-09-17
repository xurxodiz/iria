import random

import pytumblr
from telegram.ext import CommandHandler


class GifsApmHandler:

    _command_handles = ["g", "gifsapm"]

    def __init__(self):
        with open("./secret/tumblr_token", mode='r', encoding='utf-8') as f:
            [c_key, c_secret, a_token, a_secret] = [l.strip() for l in f.readlines()]

        self._tclient = pytumblr.TumblrRestClient(c_key, c_secret, a_token, a_secret)


    def register(self, dp):
        for ch in self._command_handles:
            dp.add_handler(CommandHandler(ch, self.handle, pass_args=True))


    def handle(self, bot, update, args):
        try:
            tagged_posts = self._tclient.posts('gifsapm', tag=args[0])
            gifs = self._extract_gifs_from_tumblr(tagged_posts)
        except:
            # no posts/pics for that tag
            gifs = []
        # in any case, if no gif found
        if gifs == []:
            # old man cringing
            gifs = ['http://i765.photobucket.com/albums/xx299/Daft_Punk64/APM_.gif']
        update.message.reply_document(random.choice(gifs))


    def _extract_gifs_from_tumblr(self, posts):
        candidates = [p['photos'] for p in posts['posts'] if 'photos' in p]
        urls = [u[0]['original_size']['url'] for u in candidates]
        gifs = [u for u in urls if u[-3:] == "gif"]
        return gifs




