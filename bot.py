import config
import telebot



bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(content_types = ['text'])
def lalala(message):
  bot.send_message(message.chat.id,message.text)
if __name__ == '__main__':
    bot.polling(none_stop=True)

