import telebot
import os
from telebot.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Инициализация бота
BOT_TOKEN = '7940253060:AAE6HFJGi0tbipn1nxsmnZ8lOk5ykTkK6PI' 
bot = telebot.TeleBot(BOT_TOKEN)

# Базовый URL вашего веб-приложения
WEBAPP_URL = 'https://your-domain.com'  # Замените на ваш домен

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="Открыть календарь", 
        web_app=WebAppInfo(url=f"https://your-app.onrender.com/calendar.html?user_id={message.from_user.id}&username={message.from_user.username}")
    ))
    
    bot.send_message(
        message.chat.id,
        "Нажмите кнопку ниже, чтобы открыть календарь:",
        reply_markup=markup
    )

# Обработчик для получения данных от веб-приложения
@bot.message_handler(content_types=['web_app_data'])
def web_app_handler(message):
    # Здесь можно обработать данные, полученные от веб-приложения
    try:
        data = message.web_app_data.data
        # Обработка полученных данных
        bot.send_message(
            message.chat.id,
            f"Спасибо! Ваша бронь подтверждена.\nДетали: {data}"
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            "Произошла ошибка при обработке данных."
        )

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True) 