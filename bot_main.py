from tokens import tg_bot_token as bot_token
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, Application, MessageHandler, filters, CommandHandler, Updater, \
    ConversationHandler
from tokens import map_static_api_token as static_token
import maps

MAIN, REVIEW, MARKS = [1, False], [2, False], [3, False]
LOCAL_DATA = dict()
add_review = []
add_marks = []


async def start(update: Update, context: CallbackContext):
    global LOCAL_DATA
    user_ifo = update.effective_user
    if not ('USERINFO' in LOCAL_DATA.keys()):
        LOCAL_DATA['USERINFO'] = user_ifo
    with open('help.txt', encoding='utf-8') as file:
        reply_keyboard = [['/review', 'marks']]
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
    cord = maps.coord(static_token, str(context.args[0]))
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={cord[0]},{cord[1]}&spn=0.09,0.09&l=map"
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=map_request)


def main():
    application = Application.builder().token(bot_token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('marks', marks), CommandHandler('review', review)],
        states={
            REVIEW[0]: [MessageHandler(filters.TEXT, review)],
            MARKS[0]: [MessageHandler(filters.TEXT, marks)]
        }, fallbacks=[CommandHandler('start', start)])
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("city", choose_city))
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
    print(LOCAL_DATA)
