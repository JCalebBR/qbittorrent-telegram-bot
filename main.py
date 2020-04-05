import json
import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

import torrent

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SELECTION = str()

TOKEN = os.environ.get('TOKEN')

def queue(update, context):
    status = ['downloading', 'completed', 'paused', 'active', 'inactive', 'resumed']
    reply_keyboard = [[st] for st in status]
    update.message.reply_text(
        'Choose a status:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return SELECTION

def queue_status(update, context):
    torrents = torrent.queue(update.message.text)
    for t in torrents:
        update.message.reply_text(t)
    return ConversationHandler.END

def add(update, context):
    pass

def cancel(update, context):
    return ConversationHandler.END

def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}', update, context.error)

def main():
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    queue_handler = ConversationHandler(
        entry_points=[CommandHandler('queue', queue)],

        states={
            SELECTION: [MessageHandler(Filters.text, queue_status)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    #dp.add_handler(CommandHandler("cancel", cancel))
        # log all errors
    dp.add_handler(queue_handler)
    dp.add_error_handler(error)

    updater.start_webhook(listen='0.0.0.0', 
                        port=PORT,
                        url_path=TOKEN)
    updater.bot.set_webhook("https://caleb-qbittorrent.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
