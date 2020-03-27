import logging

from telegram import ParseMode
from telegram.ext import CommandHandler

from . import rollem


commands = ["roll"]


def register(dispatcher):
    dispatcher.add_handler(CommandHandler(commands, roll))
    logging.info(f"{__package__} has registered for commands {commands}")


def roll(update, context):
    user = update.message.from_user.name

    if not context.args:
        request = ""
    else:
        request = context.args[0]

    parsed_request = interpret(request)

    try:
        result = rollem.roll(parsed_request)
        formula = result["visual"]
        total = result["total"]

        msg = f"{user} rolled {request}:\n{formula}\n= <strong>{total}</strong>"
        update.message.reply_text(msg, parse_mode=ParseMode.HTML)

    except rollem.InvalidFormatEquationException:
        logging.error("Invalid format: " + request)
        update.message.reply_text("Invalid format")


def interpret(request):
    if not request:
        return "4dF"
    else:
        return request
