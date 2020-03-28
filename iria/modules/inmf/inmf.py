import logging

from telegram.ext import CommandHandler, CallbackQueryHandler, Filters

from . import game


logger = logging.getLogger(__package__)


def register(dp):
    dp.add_handler(CallbackQueryHandler(inmf_cancel, pattern='^inmf_cancel$'))
    commands = [mod.register(dp)
                for mod in [
                    game
                ]]
    logger.info(f"Registered for commands {commands}")


def inmf_cancel(update, _context):
    update.callback_query.edit_message_text(text="No problem.")