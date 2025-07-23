import telebot

from algorithm.recommendation_algorithm import RecommendationAlgorithm
from clope_recommendations import get_user_interests_from_cluster, load_clope_model

bot = telebot.TeleBot('')

@bot.message_handler(content_types=['text'])
def start(message):
    try:
        if message.text == '/start':
            bot.send_message(message.from_user.id, "Привет! Я бот, который анализирует интересы пользователя VK. Напиши мне свой id в VK")
        elif message.text.isdigit():
            bot.send_message(message.from_user.id, "Анализирую интересы...")
            
            # Получаем интересы пользователя
            algorithm = RecommendationAlgorithm()
            interests2count = algorithm.get_interests(int(message.text))
            interests = [pair[0] for pair in interests2count]
            
            if not interests:
                bot.send_message(message.from_user.id, "К сожалению я не смог найти твоего пользователя :(\nПроверь, правильно ли введен твой id и попробуй еще раз")
                return
            
            clope = load_clope_model()
            
            cluster_interests = get_user_interests_from_cluster(clope, interests)
            
            # Формируем ответ
            response = f"Ваши топ-5 интересов:\n- " + "\n- ".join(interests) + "\n\n"
            response += f"Топ-10 интересов вашего кластера:\n- "
            response += "\n- ".join(cluster_interests)
            
            bot.send_message(message.from_user.id, response)
            
        else:
            bot.send_message(message.from_user.id, "Некорректный формат id. Введите числовой id пользователя VK.")
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.from_user.id, "Произошла ошибка. Попробуйте позже.")

@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice"])
def incorrect_format(message):
    bot.send_message(message.from_user.id, "Пожалуйста, введите числовой id пользователя VK.")

bot.polling(none_stop=True, interval=0)