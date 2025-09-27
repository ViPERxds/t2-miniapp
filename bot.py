import telebot
import os
ф
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="Открыть календарь", 
        web_app=WebAppInfo(url=f"https://viperxds.github.io/t2-miniapp/calendar.html?user_id={message.from_user.id}&username={message.from_user.username}")
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
