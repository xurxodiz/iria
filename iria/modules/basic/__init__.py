import logging

from telegram.ext import CommandHandler


commands = ["start", "help"]


def register(dispatcher):
    # default handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_))
    dispatcher.add_error_handler(error)  # log all errors
    logging.info(f"{__package__} has registered for commands {commands}")


def start(update, _context):
    update.message.reply_text("Hi! It's Iria here. Let's play!")


def help_(update, _context):
    update.message.reply_text(
        """
        Open http.//github.com/xurxodiz/iria for the README
        """)


def error(update, context):
    logging.error(f'Update "{update}" caused error "{context.error}"')