#!/usr/bin/env python3

# Based on echobot2.py


import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from modules.gifsapm import GifsApmHandler
from modules.estraviz import EstravizHandler
from modules.dice import DiceHandler


########################
# LOGGING
########################

logging.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                    level=logging.INFO,
                    filename='iria.log')

logger = logging.getLogger(__name__)


########################
# DEFAULT HANDLERS
########################

def start(bot, update):
    update.message.reply_text('Olá!')


def help(bot, update):
    update.message.reply_text(
    """
    Prova:
        /e(straviz) palavra-a-pesquisar
        /g(ifsapm) tag-do-gif
        /d(ados) jogada-de-dados
    """)


def echo(bot, update):
    update.message.reply_text(update.message.text, parse_mode="Markdown")


def error(bot, update, error):
    logger.warn('Mensagem "%s" causou erro "%s"' % (update, error))
    try:
        raise error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        logger.warn('Unauthorized: %s' % update.message.chat_id)
    except BadRequest:
        logger.warn('Bad Request')
        # handle malformed requests - read more below!
    except TimedOut:
        logger.warn('Timed Out')
        # handle slow connection problems
    except NetworkError:
        logger.warn('Network Error')
        # handle other connection problems
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        logger.warn('Chat Migrated: %s' % error.new_chat_id)
    except TelegramError:
        # handle all other telegram related errors
        logger.warn('Other Telegram Error')

    


########################
# BOT START
########################

# Open secret token
with open("./secret/bot_token", mode='r', encoding="utf-8") as f:
    tg_token = f.readline().strip()

# Create the EventHandler and pass it your bot's token.
updater = Updater(tg_token)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# default handlers
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(MessageHandler(Filters.text, echo)) # on noncommand
dp.add_error_handler(error) # log all errors

#################################
# custom modules are defined here
#################################

EstravizHandler().register(dp, logger)
GifsApmHandler().register(dp, logger)
DiceHandler().register(dp, logger)


# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
