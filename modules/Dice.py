from random import randint, seed
import re

from telegram.ext import CommandHandler


class DiceHandler:

    _command_handles = ["d", "dados"]

    def __init__(self):
        seed()
        self.regex = re.compile("([-+])?(?:(\d+)(d)?(\d+)?)", re.IGNORECASE)
        self.last = ""


    def register(self, dp):
        for ch in self._command_handles:
            dp.add_handler(CommandHandler(ch, self.handle, pass_args=True))


    def handle(self, bot, update, args):
        result = 0
        if len(args) == 0:
            msg = self.last # a reroll has been asked
        else:
            msg = args[0]
            self.last = msg # keep it for rerolls

        for match in self.regex.finditer(msg):
            if match.group(1) == "-":
                factor = -1
            else:
                factor = 1
            if match.group(3) == "d":
                value = self.roll(int(match.group(2)), int(match.group(4)))
            else:
                value = int(match.group(2))
            result += factor * value

        update.message.reply_text(str(result))


    def roll(self, num_die, sides):
        return sum([randint(1, sides) for _ in range(num_die)])