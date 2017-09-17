from urllib.request import urlopen
from urllib.parse   import quote # for utf-8

from lxml import html
from telegram.ext import CommandHandler


class EstravizHandler:

    _command_handles = ["e", "estraviz"]

    def __init__(self):
        pass


    def register(self, dp):
        for ch in self._command_handles:
            dp.add_handler(CommandHandler(ch, self.handle, pass_args=True))
    

    def handle(self, bot, update, args):
        if len(args) > 0:
            with urlopen('http://estraviz.org/' + quote(args[0])) as f:
                doc = html.parse(f)
            entry = doc.find(".//div[@id='resultado']/ol")
            if entry is not None:
                msg = "".join([t for t in self._traverse(entry)])
            else:
                msg = "Nom atopei rem"
            update.message.reply_text(msg, parse_mode="Markdown")
        else:
            update.message.reply_text("Nom entendo")


    ##########
    # Go through the nodes and produce the text and markup events
    ##########
    
    @classmethod
    def _traverse(cls, node):

        yield cls._opening(node)

        if node.text and node.text.strip():
            yield node.text

        for child in node:
            yield from cls._traverse(child)

        yield cls._closing(node)

        if node.tail and node.tail.strip():
            yield node.tail


    ##########
    # Produce appropriate opening/closing markup
    ##########

    @classmethod
    def _opening(cls, element):
        if element.tag == 'h1':
            return "\n*"
        if element.tag == 'b':
            return "*"
        elif 'chaves' in element.classes:
            return "\["
        elif element.tag == 'div':
            return "\n"
        elif element.tag == 'i' \
          and element.getparent().tag not in ('b', 'h1') \
          and 'etimologia' not in element.getparent().classes:
          # can't double markup at the moment
            return "_"
        elif element.tag == 'sub':
            return " {"
        elif 'etimologia' in element.classes \
            or ('style' in element.attrib \
                and element.attrib['style'] == "font-variant: small-caps;"):
            return "`"
        elif element.tag == 'li':
            return "\n"
        else:
            return ""


    @classmethod
    def _closing(cls, element):
        if element.tag == 'h1':
            return "* "
        if element.tag == 'b':
            return "*"
        elif 'chaves' in element.classes:
            return "]"
        elif element.tag == 'div':
            return ""
        elif element.tag == 'i' \
          and element.getparent().tag not in ('b', 'h1') \
          and 'etimologia' not in element.getparent().classes:
          # can't double markup at the moment
            return "_"
        elif element.tag == 'sub':
            return "}"
        elif 'etimologia' in element.classes \
          or ('style' in element.attrib \
          and element.attrib['style'] == "font-variant: small-caps;"):
            return "`"
        else:
            return ""

