import logging
import random
import os

import pytumblr
from telegram.ext import CommandHandler


commands = ["g", "gifsapm"]
_tclient = None


def register(dispatcher):
    global _tclient

    token_path = os.path.join(os.environ.get("DATA_DIR"), "secret", "tumblr_token")
    with open(token_path, encoding='utf-8') as f:
        [c_key, c_secret, a_token, a_secret] = [l.strip() for l in f.readlines()]

    _tclient = pytumblr.TumblrRestClient(c_key, c_secret, a_token, a_secret)
    dispatcher.add_handler(CommandHandler(commands, post_gif))
    logging.info(f"{__package__} has registered for commands {commands}")


def post_gif(update, context):
    txt = context.args[1]
    try:
        tagged_posts = _tclient.posts('gifsapm', tag=txt)
        gifs = _extract_gifs_from_tumblr(tagged_posts)

    except Exception as e:
        logging.error("Error: " + repr(e))
        # no posts/pics for that tag
        gifs = []

    # in any case, if no gif found:
    if not gifs:
        # old man cringing
        logging.info("No gifs found for: " + txt)
        gifs = ['http://i765.photobucket.com/albums/xx299/Daft_Punk64/APM_.gif']

    update.message.reply_document(random.choice(gifs))


def _extract_gifs_from_tumblr(posts):
    candidates = [p['photos'] for p in posts['posts'] if 'photos' in p]
    urls = [u[0]['original_size']['url'] for u in candidates]
    gifs = [u for u in urls if u[-3:] == "gif"]
    return gifs
