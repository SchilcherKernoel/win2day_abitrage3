import logging
from flask import Flask
from Make_Data_Strucutre import *
from Make_URL import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from New_Bet import make_bet
from Make_Slip import make_slip
from Bundle_Slips import *
from Demark_Bets import *


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
SAVE_ERASE = range(1)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def get(update, context):
    """Send a message when the command /get is issued."""
    mds_status = make_data_structure()
    if mds_status != 1:
        update.message.reply_text(mds_status)
        return

    mu_status = make_url()
    if mu_status != 1:
        update.message.reply_text(mu_status)
        return
    else:
        update.message.reply_text('URL file is now available')


def bet(update, context):
    """Send a message when the command /bet is issued."""
    update.message.reply_text('Making bets!')
    failed, tried = make_bet()
    update.message.reply_text('Program tried to match '+str(tried)+' bets')
    update.message.reply_text('Program failed to match '+str(failed)+' bets')


def slip(update, context):
    """Send a message when the command /bet is issued."""
    update.message.reply_text('Making slips!')
    update.message.reply_text(make_slip(minimum_diff, maximum_diff, minimum_qoute, maximum_qoute))


def slip_check(update, context):
    """Send a message when the command slip_checkis issued."""
    chat_id = update.message.chat_id
    document = open(get_working_directory()+slip_file_name)
    context.bot.send_document(chat_id, document)


def help(update, context):
    update.message.reply_text('Make data structure /get')
    update.message.reply_text('Get betting data: /bet')
    update.message.reply_text('Make betting slips: /slip')
    update.message.reply_text('Get CSV of slips: /slip_check')
    update.message.reply_text('Get bundles of 3 of bets: /bundle')
    update.message.reply_text('remove demarkation: /demark')

def bundle(update, context):
    i = bundle_slips()
    #if not slip_list:
        #update.message.reply_text('no unmarked bets available')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def demark(update, context):
    demark_bets()
    update.message.reply_text('demarking bets')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(telgegram_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("get", get))
    dp.add_handler(CommandHandler("bet", bet))
    dp.add_handler(CommandHandler("slip", slip))
    dp.add_handler(CommandHandler("slip_check", slip_check))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("bundle", bundle))
    dp.add_handler(CommandHandler("demark", demark))

    # on no command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


app = Flask(__name__)
if __name__ == '__main__':
    main()
