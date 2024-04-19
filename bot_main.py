from tokens import tg_bot_token as token
import logging
from telegram._update import Update
from telegram.ext._callbackcontext import CallbackContext
from telegram.ext import Application, MessageHandler, filters, CommandHandler

# логи кода
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: CallbackContext):  # помощь пользователю
    with open('help.txt', encoding='utf-8') as file:
        await update.message.reply_text(''.join(file.readlines()))


async def registration(update: Update, context: CallbackContext):  # регистрация почты пользователя
    await update.message.reply_text('')


async def choose_city(update: Update, context: CallbackContext):  # выбор города для путешествия
    await update.message.reply_text('')


async def look_at_attractions(update: Update, context: CallbackContext):  # просмотр достопремичательностей
    await update.message.reply_text('')


async def look_at_hotels(update: Update, context: CallbackContext):  # просмотр отелей
    await update.message.reply_text('')


async def look_at_tickets(update: Update, context: CallbackContext):  # поиск билетов до города
    await update.message.reply_text('')


async def book_hotel(update: Update, context: CallbackContext):  # бронирование билетов
    await update.message.reply_text('')


async def buy_ticket(update: Update, context: CallbackContext):  # покупка билетов до города
    await update.message.reply_text('')


def main():
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reg", registration))
    application.add_handler(CommandHandler("city", choose_city))
    application.add_handler(CommandHandler("attractions", look_at_attractions))
    application.add_handler(CommandHandler("hotels", look_at_hotels))
    application.add_handler(CommandHandler("tickets", look_at_tickets))
    application.add_handler(CommandHandler("book_hotel", book_hotel))
    application.add_handler(CommandHandler("buy_ticket", buy_ticket))

    application.run_polling()


if __name__ == '__main__':
    main()
