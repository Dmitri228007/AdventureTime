from tokens import tg_bot_token as bot_token
from telegram._update import Update
from telegram.ext._callbackcontext import CallbackContext
from telegram.ext import Application, MessageHandler, filters, CommandHandler, Updater
from tokens import map_static_api_token as static_token
import requests
import maps
import os


async def help_command(update: Update, context: CallbackContext):  # помощь пользователю
    with open('help.txt', encoding='utf-8') as file:
        await update.message.reply_text(''.join(file.readlines()))


async def registration_(update: Update, context: CallbackContext):  # регистрация почты пользователя
    await update.message.reply_text('введите свою почту для того чтобы вам приходили туда ваши купленные билеты')


async def registration_form(update: Update, context: CallbackContext):  # регистрация почты пользователя
    print(update.message.text)
    # await update.message.reply_text(f'{context.args}')


async def choose_city(update: Update, context: CallbackContext):  # выбор города для путешествия
    func_args = context.args
    city = str(func_args[0])
    chat_id = update.message.chat_id
    cord = maps.coord(static_token, city)
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={cord[0]},{cord[1]}&spn=0.09,0.09&l=map"
    await context.bot.send_photo(chat_id=chat_id, photo=map_request)


async def look_at_attractions(update: Update, context: CallbackContext):  # просмотр достопремичательностей
    await update.message.reply_text('command')


async def look_at_hotels(update: Update, context: CallbackContext):  # просмотр отелей
    await update.message.reply_text('command')


async def look_at_tickets(update: Update, context: CallbackContext):  # поиск билетов до города
    await update.message.reply_text('command')


async def book_hotel(update: Update, context: CallbackContext):  # бронирование билетов
    await update.message.reply_text('command')


async def buy_ticket(update: Update, context: CallbackContext):  # покупка билетов до города
    await update.message.reply_text('command')


def main():
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registration_form))
    application.add_handler(CommandHandler("reg", registration_))
    application.add_handler(CommandHandler("city", choose_city))
    application.add_handler(CommandHandler("attractions", look_at_attractions))
    application.add_handler(CommandHandler("hotels", look_at_hotels))
    application.add_handler(CommandHandler("tickets", look_at_tickets))
    application.add_handler(CommandHandler("book_hotel", book_hotel))
    application.add_handler(CommandHandler("buy_ticket", buy_ticket))

    application.run_polling()


if __name__ == '__main__':
    main()
