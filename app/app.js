const path = require('path');
const fs = require('fs');
const TelegramBot = require('node-telegram-bot-api');
const inkjs = require('inkjs');
const token = require('./secrets/token.json').token;

const bot = new TelegramBot(token, {polling: true});

const kbdMessage = {};
const inkStory = {};
// TODO: multiplex this by chatId
// probably combine it with kbdMessage above
let fromChoice = false;

const gameFile = path.resolve(__dirname, 'ink/game.ink.json');
const json = fs.readFileSync(gameFile, 'UTF-8').replace(/^\uFEFF/, '');

function sendMessageWithKbd (chatId, text, inline_keyboard) {
  bot.sendMessage(chatId, text, {
    parse_mode: 'Markdown',
    one_time_keyboard: true,
    reply_markup: { inline_keyboard: inline_keyboard }
  })
  .then((msg) => { kbdMessage[chatId] = msg.message_id; });
}

function getScene(chatId) {
  let text = '';
  let choices = [];
  while (inkStory[chatId].canContinue) {
    inkStory[chatId].Continue();
    let tidbit = inkStory[chatId].currentText;
    if (fromChoice) {
      text += '*' + tidbit + '*';
      fromChoice = false;
    } else {
      text += tidbit;
    }
  }
  inkStory[chatId].currentChoices.forEach((choice, id) => {
    choices.push( [{text: choice.text, callback_data: id}] );
  });
  if (!choices.length) {
    bot.sendMessage(chatId, text, { parse_mode: 'Markdown' })
    .then(
      // TODO: Add not-inline keyboard with big START button to begin again
      () => bot.sendMessage(chatId, '```\nFIN.\n```', { parse_mode: 'Markdown' })
    );
    return;
  }
  sendMessageWithKbd(chatId, text || '.', choices);
}

bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  if (msg.text === '/start') {
    inkStory[chatId] = new inkjs.Story(json);
    bot.sendMessage(chatId, '```\nLet us begin.\n```', { parse_mode: 'Markdown' }).then (
      () => getScene(chatId)
    );
  } else {
    bot.sendMessage(chatId, '```\nSay "/start" to start game.\n```', { parse_mode: 'Markdown' });
  }
});

bot.on('callback_query', (res) => {
  const data = res.data;
  const chatId = res.message.chat.id;
  bot.editMessageReplyMarkup(
    { reply_markup: null },
    {
      chat_id: chatId, 
      message_id: res.message.message_id
    }
  ).then(() => {
    if (kbdMessage[chatId]) {
        kbdMessage[chatId] = null;
        // TODO: try catch this option
        inkStory[chatId].ChooseChoiceIndex(data);
        fromChoice = true;
        getScene(chatId);
    } else {
      // TODO: come here from future catch above
      bot.sendMessage(chatId, '```\n…Truth be told, I forgot where I was.\n```', { parse_mode: 'Markdown' });
    }
  })
});

bot.on("polling_error", (err) => console.error(err));
