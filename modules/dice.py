from random import randint, seed
import re

from telegram.ext import CommandHandler


class DiceHandler:

    _command_handles = ["d", "dados"]

    def __init__(self):
        seed()
        self.regex = re.compile("(^|[-+])(?:(\d{1,3})(d(\d{0,3}))?)", re.IGNORECASE)
        self.last = ""


    def register(self, dp, logger):
        for ch in self._command_handles:
            dp.add_handler(CommandHandler(ch, self.handle, pass_args=True))
        self.logger = logger


    def handle(self, bot, update, args):
        if len(args) == 0:
            msg = self.last # a reroll has been asked
        else:
            msg = args[0]

        canon = ""
        result = 0
        for i, match in enumerate(self.regex.finditer(msg)):
            if i > 5:
                # someone messing, probably
                break

            if match.group(1) == "-":
                factor = -1
            else:
                factor = 1
            canon += match.group(1)

            if match.group(3):
                value = self.roll(int(match.group(2)), int(match.group(4)))
                canon += match.group(2) + "d" + match.group(4)
            else:
                value = int(match.group(2))
                canon += match.group(2)

            result += factor * value
        
        self.last = canon  # keep it for rerolls
        self.logger.info("[DD] A rolar: %s, canonizado: %s, resultado: %s" % (msg, canon, result))
        update.message.reply_text(canon + " = " + str(result))


    def roll(self, num_die, sides):
        return sum([randint(1, sides) for _ in range(num_die)])