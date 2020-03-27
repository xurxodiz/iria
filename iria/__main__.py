#!/usr/bin/env python3

import importlib
import logging
import os

from telegram.ext import Updater


# Set up logging output
logging.basicConfig(format='[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s',
                    level=logging.INFO,
                    filename='iria.log')

logging.info("Starting up!")

# Read auth token
token_path = os.path.join(os.environ.get("DATA_DIR"), "secret", "bot_token")
logging.info('Reading Telegram token from "' + token_path + '" ...')
with open(token_path, encoding="utf-8") as f:
    token = f.readline().strip()

# Create the Updater
updater = Updater(token, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Dynamically load plugins
# Any folder inside "modules"
# that contains a __init__.py
# and whose name is not included in data/disabled
# will be loaded and its method "register" called
# (receiving as only parameter the dispatcher)
logging.info("Dynamically loading plugins...")
importlib.import_module(__package__ + '.modules')
module_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'modules')
with os.scandir(module_folder) as it:
    for entry in it:
        if entry.is_dir() \
                and os.path.exists(os.path.join(module_folder, entry.name, "__init__.py")):
            module_full_ref = __package__ + ".modules." + entry.name
            try:
                module = importlib.import_module(module_full_ref)
                module.register(dispatcher)
            except ModuleNotFoundError:
                logging.error(module_full_ref + " is not a valid module, could not load")
            except AttributeError:
                logging.error(module_full_ref + " has no register method, could not hook")
            except Exception:
                logging.error(module_full_ref + " has caused an error while registering, could not hook")

# Start the Bot
logging.info("Starting to poll...")
updater.start_polling()
logging.info("Polling.")

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
