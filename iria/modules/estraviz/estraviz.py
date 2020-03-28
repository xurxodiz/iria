import logging
from urllib.request import urlopen
from urllib.parse import quote  # for utf-8

from lxml import html
from telegram.ext import CommandHandler


commands = ["e", "estraviz"]
logger = logging.getLogger(__package__)


def register(dp):
    dp.add_handler(CommandHandler(commands, procura))
    logger.info(f"Registered for commands {commands}")


def procura(update, context):
    if not context.args:
        update.message.reply_text("Não entendo")
        return

    try:
        with urlopen('http://estraviz.org/' + quote(context.args[0])) as f:
            doc = html.parse(f)
    except IOError as e:
        logger.error("Cannot connect: " + e.args)
        update.message.reply_text("Nõa pudem conectar")

    matches = doc.findall(".//div[@id='resultado']/ol")
    if matches is not None:
        msg = "".join([output for lemma in matches for output in traverse(lemma)])
    else:
        msg = "Não encontrei rem"

    update.message.reply_text(msg, parse_mode="Markdown")


##########
# Go through the nodes and produce the text and markup events
##########

def traverse(node):

    yield opening(node)

    if node.text and node.text.strip():
        yield node.text

    for child in node:
        yield from traverse(child)

    yield closing(node)

    if node.tail and node.tail.strip():
        yield node.tail


##########
# Produce appropriate opening/closing markup
##########

def opening(element):
    if element.tag == 'h1':
        return "\n*"
    elif element.tag == 'b':
        return '*'
    elif 'chaves' in element.classes:
        return r'\['
    elif 'formaVerbo' in element.classes:
        return "*"
    elif 'infinito' in element.classes:
        return '_'
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
            or ('style' in element.attrib
                and element.attrib['style'] == "font-variant: small-caps;"):
        return "`"
    elif element.tag == 'li':
        return "\n"
    elif element.tag == 'hr':
        return "\n"
    else:
        return ""


def closing(element):
    if element.tag == 'h1' and element.text and element.text[-1] == "-":
        return "*\n"
    elif element.tag == 'h1':
        return "* "
    elif element.tag == 'b':
        return "*"
    elif 'chaves' in element.classes:
        return "]"
    elif 'formaVerbo' in element.classes:
        return "*"
    elif 'infinito' in element.classes:
        return '_'
    elif 'id' in element.attrib and element.attrib['id'] == 'tempos':
        return "\n"
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
            or ('style' in element.attrib
                and element.attrib['style'] == "font-variant: small-caps;"):
        return "`"
    else:
        return ""
