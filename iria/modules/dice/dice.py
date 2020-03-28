import logging

from telegram import ParseMode
from telegram.ext import CommandHandler

from . import rollem

commands = ["roll"]
logger = logging.getLogger(__package__)


def register(dp):
    dp.add_handler(CommandHandler(commands, roll))
    logger.info(f"Registered for commands {commands}")


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
        logger.error("Invalid format: " + request)
        update.message.reply_text("Invalid format")


def interpret(request):
    if not request:
        return "4dF"
    else:
        return request
