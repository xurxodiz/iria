import logging

from telegram.ext import CallbackQueryHandler

from . import game, inmf


logger = logging.getLogger(__package__)


def register(dp):
    dp.add_handler(CallbackQueryHandler(fate_cancel, pattern='^fate_cancel$'))
    commands = [mod.register(dp)
                for mod in [
                    game,
                ]]
    logger.info(f"Registered for commands {commands}")


def fate_cancel(update, _context):
    update.callback_query.edit_message_text(text="No problem.")