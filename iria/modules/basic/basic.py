import logging

from telegram.ext import CommandHandler

commands = ["start", "help"]
logger = logging.getLogger(__package__)


def register(dp):
    # default handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_))
    dp.add_error_handler(error)  # log all errors
    logger.info(f"Registered for commands {commands}")


def start(update, _context):
    update.message.reply_text("Hi! It's Iria here. Let's play!")


def help_(update, _context):
    update.message.reply_text(
        """
        Open http.//github.com/xurxodiz/iria for the README
        """)


def error(update, context):
    logger.error(f'Update "{update}" caused error "{context.error}"')