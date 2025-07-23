import pickle
from clope import CLOPE


def load_clope_model(repulsion=1.1, stopLimit=0) -> CLOPE.CLOPE:
    filename = f'src/data/CLOPE_users.r={repulsion}.stopLimit={str(stopLimit)}.pickle'
    with open(filename, 'rb') as f:
        return pickle.load(f)
    
# Функция для определения кластера пользователя
def get_user_interests_from_cluster(clope_model: CLOPE.CLOPE, user_interests: list) -> list:
    # Добавляем пользователя в модель
    cluster_id = clope_model.move_transaction(user_interests, clope_model.count_transactions + 1, repulsion=1.1)
    
    cluster = clope_model.clusters[cluster_id]
    
    interests = list(cluster.histogram.keys())
    counts = list(cluster.histogram.values())

    # Соединяем интересы и их количество в словарь, затем сортируем по убыванию
    interests_dict = dict(zip(interests, counts))
    sorted_interests = sorted(interests_dict.items(), key=lambda item: item[1], reverse=True)[:10]  # Топ-10

    # Разделяем обратно на интересы и количество
    top_interests, top_counts = zip(*sorted_interests)

    return top_interests