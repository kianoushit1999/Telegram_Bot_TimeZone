from telegram.ext import Updater, ConversationHandler, CommandHandler, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup
import logging
from GetTime import *

BASE, CHOOSING = range(2)
show_list = [
    ["Choose Country", "Show TimeZone"],
    ["Contact Developer", "Exit Bot"]
]
reply = ReplyKeyboardMarkup(show_list, one_time_keyboard=True)
country_state = ReplyKeyboardMarkup(get_list_country(), one_time_keyboard=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='telegram_bot.log')

def start(update, context):
    logging.info('Show pre-define list for choosing')
    update.message.reply_text("Hi, I hope you will be best\n"
                              "Choose which one you want\n"
                              "If you face problem contact Developer\n",
                              reply_markup=reply)
    return BASE

def country(update, context):
    logging.info('show list of pre-define country from target website')
    update.message.reply_text("Hi, Good to see you\n"
                              "Please enter your country that you want its timezone\n"
                              "Please write start to start it", reply_markup=country_state)
    return CHOOSING

def set_country(update, context):
    logging.warning('The capital that you\'ve chosen must be in list.')
    country_name = update.message.text
    context.user_data['country'] = country_name
    logging.info('Showing your decision that you made')
    update.message.reply_text("It\'s chosen :: Country name is : %s" %(country_name)
                              , reply_markup=reply)
    return BASE

def show(update, context):
    logging.info('For show information depends on you input value')
    text = update.message.text
    if text == 'Contact Developer':
        logging.info('Showing Developer information')
        update.message.reply_text("Developer is : Kianoush NasrAzadani\n Email:kianoushit1999@gmail.com\n"
                              "GitLab&Telegram id: @kianoushit1999", reply_markup=reply)
    else:
        logging.info('Showing exact timezone of capital of country which you\'re chosen')
        user_data = context.user_data
        update.message.reply_text("The timezone of %s is %s"
                                  % (user_data['country'], scraping_time()[user_data['country']])
                                  , reply_markup=reply)
    return BASE

def exit_bot(update, context):
    logging.info('The action of the bot going to end.')
    update.message.reply_text('You choose your countries you want to see its timezone\nGod bless you\nGoodbye')
    return ConversationHandler.END


def main():
    logging.info('Start action of the my telegram bot now')
    updater = Updater(token="1317092751:AAGGYcnGmN4gGeIw4NDouPDpph9j9gUoU6w", use_context=True)
    pd = updater.dispatcher

    conv_hand = ConversationHandler(

        entry_points=[CommandHandler('start', start)],

        states={
            BASE:  [MessageHandler(Filters.regex('^(Choose Country)$'), country),
            MessageHandler(Filters.regex('^(Show TimeZone|Contact Developer)$'), show)],

            CHOOSING:[MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Exit$')), set_country)],
        },
        fallbacks=[MessageHandler(Filters.regex('^Exit Bot$'), exit_bot)]
    )

    logging.info('start using new handler for begin the action of the bot')
    pd.add_handler(conv_hand)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    logging.debug('Debugging of our file is just started now')
    main()
    logging.info('Your action was ended.')