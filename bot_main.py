from tokens import tg_bot_token as bot_token
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton

from telegram.ext import CallbackContext, Application, MessageHandler, filters, CommandHandler, Updater, \
    ConversationHandler
from tokens import map_static_api_token as static_token
import maps
from place_handler import question_info
from tokens import giga_chat
from paint import *

MAIN, REVIEW, MARKS, CITY = [1, False], [2, False], [3, False], [4, False, {}]
LOCAL_DATA = dict()
add_review = []
add_marks = []


async def start(update: Update, context: CallbackContext):
    global LOCAL_DATA
    user_ifo = update.effective_user
    if not ('USERINFO' in LOCAL_DATA.keys()):
        LOCAL_DATA['USERINFO'] = user_ifo
    with open('start.txt', encoding='utf-8') as file:
        reply_keyboard = [[KeyboardButton('/help')], [KeyboardButton('/city')],
                          [KeyboardButton('/review'), KeyboardButton('/marks')]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        await update.message.reply_text(''.join(file.readlines()), reply_markup=markup)
    return ConversationHandler.END


async def review(update: Update, context: CallbackContext):
    global add_review
    global LOCAL_DATA
    if not REVIEW[1]:
        with open('review.txt', encoding='utf-8') as file:
            await update.message.reply_text(''.join(file.readlines()), reply_markup=ReplyKeyboardRemove())
    user_text = update.message.text
    if not ('REVIEW' in LOCAL_DATA.keys()):
        LOCAL_DATA['REVIEW'] = []
    if '#Отзыв' in user_text:
        REVIEW[1] = False
        add_local_data = LOCAL_DATA['REVIEW']
        add_local_data.append(context.user_data['review'])
        LOCAL_DATA['REVIEW'] = add_local_data
        add_review = []
        return ConversationHandler.END
    else:
        REVIEW[1] = True
        try:
            add_review.append(user_text)
            context.user_data['review'] = add_review
        except KeyError:
            context.user_data['review'] = user_text
        return REVIEW[0]


async def marks(update: Update, context: CallbackContext):
    global add_marks
    global LOCAL_DATA
    if not MARKS[1]:
        with open('marks.txt', encoding='utf-8') as file:
            await update.message.reply_text(''.join(file.readlines()), reply_markup=ReplyKeyboardRemove())
    user_text = update.message.text
    if not ('MARKS' in LOCAL_DATA.keys()):
        LOCAL_DATA['MARKS'] = []
    if '#Заметки' in user_text:
        MARKS[1] = False
        add_local_data = LOCAL_DATA['MARKS']
        add_local_data.append(context.user_data['marks'])
        LOCAL_DATA['MARKS'] = add_local_data
        add_marks = []
        return ConversationHandler.END
    else:
        MARKS[1] = True
        try:
            add_marks.append(user_text)
            context.user_data['marks'] = add_marks
        except KeyError:
            context.user_data['marks'] = user_text
        return MARKS[0]


async def choose_city(update: Update, context: CallbackContext):
    user_text = update.message.text
    await update.message.reply_text(giga_chat(user_text))
    # global CITY
    # if not CITY[1]:
    #     await update.message.reply_text('Напишите название города который вы хотели бы посетить')
    #     CITY[1] = True
    #     return CITY[0]
    # elif CITY[1] and not ('selected city' in CITY[2].keys()):
    #     user_city = update.message.text
    #     CITY[2]['selected city'] = user_city
    #     cord = maps.coord(static_token, str(CITY[2]['selected city']))
    #     map_request = f"http://static-maps.yandex.ru/1.x/?ll={cord[0]},{cord[1]}&spn=0.09,0.09&l=map"
    #     await context.bot.send_photo(chat_id=update.message.chat_id, photo=map_request)
    #     reply_keyboard = [[KeyboardButton('Посмотреть отели'), KeyboardButton('Посмотреть достопримечательности')],
    #                       [KeyboardButton('Узнать цены на билеты')],
    #                       [KeyboardButton('Другой город'), KeyboardButton('В главное меню')]]
    #     markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    #     await update.message.reply_text('Что будем планировать?', reply_markup=markup)
    #     return CITY[0]
    # elif update.message.text == 'Посмотреть отели':
    #     print(question_info(f'''{CITY[2]['selected city']}Отели'''))
    #     return CITY[0]
    #
    # elif update.message.text == 'Посмотреть достопримечательности':
    #     print('Посмотреть достопримечательности')
    #     return CITY[0]
    #
    # elif update.message.text == 'Узнать цены на билеты':
    #     print('Узнать цены на билеты')
    #     return CITY[0]
    #
    # elif update.message.text == 'Другой город':
    #     CITY = [4, False, {}]
    #     return CITY[0]
    #
    # elif update.message.text == 'В главное меню':
    #     return MAIN[0]
    #


def main():
    application = Application.builder().token(bot_token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('marks', marks), CommandHandler('review', review),
                      CommandHandler("city", choose_city), CommandHandler("start", start)],
        states={
            MAIN[0]: [MessageHandler(filters.TEXT, start)],
            REVIEW[0]: [MessageHandler(filters.TEXT, review)],
            MARKS[0]: [MessageHandler(filters.TEXT, marks)],
            CITY[0]: [MessageHandler(filters.TEXT, choose_city)]
        }, fallbacks=[CommandHandler('start', start)])
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
    print(LOCAL_DATA)
