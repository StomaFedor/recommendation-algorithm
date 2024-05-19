import telebot

from algorithm.recommendation_algorithm import RecommendationAlgorithm

bot = telebot.TeleBot('')

@bot.message_handler(content_types=['text'])
def start(message):
    try:
        if message.text == '/start':
            bot.send_message(message.from_user.id, "Привет! Я бот, который умеет анализировать интересы пользователя и рекомендовать группы в социальной сети VK. Напиши мне свой id")
        elif message.text.isdigit():
            bot.send_message(message.from_user.id, "Подожди секунду\nИщу подходящие группы")
            algorithm = RecommendationAlgorithm()
            links = algorithm.get_recommendations(int(message.text))
            if links == None:
                bot.send_message(message.from_user.id, "К сожалению я не смог найти твоего пользователя :(\nПроверь, правильно ли введен твой id и попробуй еще раз")
                return
            
            result_str = 'Рекомендованные группы:\n'
            for link in links:
                result_str += link + '\n'
            bot.send_message(message.from_user.id, result_str)
            print("Для пользователя подобраны группы, user_id = " + str(message.from_user.id))
        else:
            bot.send_message(message.from_user.id, "Ты ввел некорректный формат id. Проверь, все ли введено правильно и попробуй еще раз :)\nПример id пользователя: 123123")
    except:
        bot.send_message(message.from_user.id, "Ой, произошла какая-то ошибка...\nПопробуй, пожалуйста, еще раз")
        print("Ошибка при подборе рекоммендаций user_id = " + str(message.from_user.id))

@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice"])
def incorrect_format(message):
    bot.send_message(message.from_user.id, "К сожалению, я не поддерживаю такой формат сообщений :(\nПопробуй ввести id пользователя из VK, а я тебе порекомендую интересные ему группы")

bot.polling(none_stop=True, interval=0)