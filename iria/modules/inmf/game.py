import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler

from .db import DB, GameRunningError, GameNotRunningError


logger = logging.getLogger(__package__)

commands = ["game"]


def register(dp):
    dp.add_handler(CommandHandler(commands, game))
    dp.add_handler(CallbackQueryHandler(game_start, pattern='^game_start$'))
    dp.add_handler(CallbackQueryHandler(game_info, pattern='^game_info$'))
    dp.add_handler(CallbackQueryHandler(game_end, pattern='^game_end$'))
    return commands


def game(update, context):
    try:
        running = DB().is_game_running(update.effective_chat.id)

        if len(context.args) == 0:
            if running:
                keyboard = [
                    [InlineKeyboardButton("Show game info", callback_data='game_info')],
                    [InlineKeyboardButton("End game", callback_data='game_end')]
                ]
            else:
                keyboard = [
                    [InlineKeyboardButton("Start a game", callback_data='game_start')]
                ]
            keyboard += [[InlineKeyboardButton("<Cancel>", callback_data='inmf_cancel')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text('What do you want to do?', reply_markup=reply_markup)

        elif context.args[0] == "start":
            response = game_start_(update.effective_chat.id, update.effective_user.id, update.effective_user.name)
            update.message.reply_text(response)

        elif context.args[0] == "info":
            response = game_info_(update.effective_chat.id)
            update.message.reply_text(response)

        elif context.args[0] == "end":
            response = game_end_(update.effective_chat.id, update.effective_user.id)
            update.message.reply_text(response)

    except GameRunningError:
        update.message.reply_text("Game is already running!")
    except GameNotRunningError:
        update.message.reply_text("Game is not running!")


def game_start(update, _context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    response = game_start_(chat_id, user_id, user_name)
    update.callback_query.edit_message_text(text=response)


def game_start_(chat_id, user_id, user_name):
    DB().do_game_start(chat_id, user_id, user_name)
    return f"Game started by {user_name}!"


def game_end(update, _context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    response = game_end_(chat_id, user_id)
    update.callback_query.edit_message_text(text=response)


def game_end_(chat_id, user_id):
    if DB().is_game_master(chat_id, user_id):
        DB().do_game_end(chat_id)
        return "Game ended. Well played!"
    else:
        return "You are not the master: you can't end the game!"


def game_info(update, _context):
    chat_id = update.effective_chat.id
    response = game_info_(chat_id)
    update.callback_query.edit_message_text(text=response)


def game_info_(chat_id):
    players = DB().get_game_players(chat_id)
    return 'The current game has the following players:\n' + \
           ''.join([
            f"{player.user_name} ({player.role})\n"
            for player in players
           ])
