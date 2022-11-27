const path = require('path');
const fs = require('fs');
const TelegramBot = require('node-telegram-bot-api');
const inkjs = require('inkjs');
const token = require('./secrets/token.json').token;


// interface strings
const TXT_LETS_BEGIN = 'A historia di así:';
const TXT_UNKNOWN = 'Non sei que me queres dicir con iso.';
const TXT_OK_RESTART = 'Está ben, comezarei de novo.';
const TXT_SAY_START = 'Pulsa o botón e cóntoche desde o comezo.';
const TXT_I_FORGOT = '…A verdade é que xa esquecín por onde ía.';
const TXT_THE_END = 'FIN';
const BTN_START = 'Cóntame un conto!';
// hardcoded by Telegram as command autosent on first chat open
// also helpful to define as option in menu in Botfather
const CMD_START = '/start';

// internal, not printed
const ERR_CHOICE_UNEXPECTED = 'Choice not expected'

// stores the status multiplexed for each chat
// see startStory() below
const state = {};

// load story json (as text)
const gameFile = path.resolve(__dirname, 'ink/game.ink.json');
const gameString = fs.readFileSync(gameFile, 'UTF-8').replace(/^\uFEFF/, '');

// connect to telegram
const bot = new TelegramBot(token, {polling: true});


// define Telegram hooks
bot.on('message', botMessage);
bot.on('callback_query', botCallbackQuery);
bot.on("polling_error", botPollingError);


//
// main hooks
//

function botMessage(msg) {
    const chatId = msg.chat.id;
    const msgText = msg.text;

    switch (msgText) {
        case CMD_START:
        case BTN_START:
            if (isStoryOngoing(chatId)) {
                speakAsIria(chatId, TXT_OK_RESTART);
                endStory(chatId);
            }
            startStory(chatId);
            speakAsIriaAndClearButtons(chatId, TXT_LETS_BEGIN)
            .then (() =>
                traverseScenesUntilChoice(chatId)
            );
            break;
        default:
            speakAsIria(chatId, TXT_UNKNOWN)
            .then(() =>
                speakAsIriaWithStartButton(chatId, TXT_SAY_START)
            );
    }
}

function botCallbackQuery(res) {
    const choiceId = res.data;
    const chatId = res.message.chat.id;
    const msgId = res.message.message_id;

    retireChoicesForMessage(chatId, msgId)
    .then(() => {
        try {
            if (!isThisChoiceExpected(chatId, msgId)) {
                throw new Error(ERR_CHOICE_UNEXPECTED);
            }
            setUserJustChose(chatId, true);
            setNoChoiceAsExpected(chatId);
            makeChoiceInStory(chatId, choiceId);
            traverseScenesUntilChoice(chatId);

        } catch (err) {
            // choice is either unexpected (old message) or not recognized by ink (?)
            speakAsIria(chatId, TXT_I_FORGOT);
            speakAsIriaWithStartButton(chatId, TXT_SAY_START);
        }
    });
}

function botPollingError(err) {
    console.error(err);
}


//
// methods for advancing the story
//

function startStory(chatId) {
    state[chatId] = {
        inkStory: new inkjs.Story(gameString),
        fromChoice: false,
        pendingChoiceMsg: null
    }
}

function endStory(chatId) {
    state[chatId] = {
        inkStory: null,
        fromChoice: false,
        pendingchoiceMsg: null
    };
}

function isStoryOngoing(chatId) {
    return state[chatId] && state[chatId].inkStory;
}

function makeChoiceInStory(chatId, choiceId) {
    state[chatId].inkStory.ChooseChoiceIndex(choiceId);
}

function traverseScenesUntilChoice(chatId) {
    let story = state[chatId].inkStory;

    let text = '';
    while (story.canContinue) {
        story.Continue();
        let tidbit = story.currentText;
        if (didUserJustChoose(chatId)) {
            text += emphasizeText(tidbit);
            setUserJustChose(chatId, false);
        } else {
            text += tidbit;
        }
    }

    let choices = [];
    story.currentChoices.forEach((choice, id) => {
	    choices.push( [{text: choice.text, callback_data: id}] );
    });

    if (choices.length) {
        speakAsStoryWithChoices(chatId, text, choices)
        .then((msg) => 
            setChoiceAsExpected(chatId, msg.message_id)
        );

    } else {
        // can't continue anymore but no choices: end of story
        speakAsStory(chatId, text)
        .then(() =>
            endStory(chatId)
        )
        .then(() =>
            speakAsIriaWithStartButton(chatId, TXT_THE_END)
        );
    }
}

// used to bold the first message after a choice is made

function didUserJustChoose(chatId) {
    return state[chatId].fromChoice;
}

function setUserJustChose(chatId, bool) {
    state[chatId].fromChoice = bool;
}

// used to process callbacks if proper or discard if for an old knot/story

function isThisChoiceExpected(chatId, msgId) {
    return state[chatId].pendingChoiceMsg === msgId;
}

function setChoiceAsExpected(chatId, msgId) {
    state[chatId].pendingChoiceMsg = msgId;
}

function setNoChoiceAsExpected(chatId) {
    state[chatId].pendingChoiceMsg = null;
}


//
// methods for printing to telegram
//

function speakAsIria(chatId, text, extraOpts = {}) {
    const defaultOpts = { parse_mode: 'Markdown' };
    const finalOpts = {...defaultOpts, ...extraOpts};
    const fmtText = '```\n' + (text || '…') + '\n```';
    return bot.sendMessage(chatId, fmtText, finalOpts);
}

function speakAsIriaWithStartButton(chatId, text) {
    const extraOpts = {
        reply_markup: {
            keyboard: [ [ { text: BTN_START } ] ],
            resize_keyboard: true,
        }
    };
    return speakAsIria(chatId, text, extraOpts);
}

function speakAsIriaAndClearButtons(chatId,  text) {
    const extraOpts = {
        reply_markup: {
            remove_keyboard: true
        }
    };
    return speakAsIria(chatId, text, extraOpts);
}

function speakAsStory(chatId, text, extraOpts = {}) {
    const defaultOpts = { parse_mode: 'Markdown' };
    const finalOpts = {...defaultOpts, ...extraOpts};
    return bot.sendMessage(chatId, text, finalOpts);
}

function speakAsStoryWithChoices(chatId, text, choices) {
    const extraOpts = {
        reply_markup: {
            inline_keyboard: choices
        }
    };
    return speakAsStory(chatId, text, extraOpts);
}

function retireChoicesForMessage(chatId, msgId) {
    return bot.editMessageReplyMarkup(
        { reply_markup: null },
        {
            chat_id: chatId, 
            message_id: msgId
        }
    );
}

function emphasizeText(txt) {
    return '*' + txt + '*';
}
