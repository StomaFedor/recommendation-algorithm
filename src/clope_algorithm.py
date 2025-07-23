from clope import CLOPE
import pickle
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

stop_words = { "жизнь", "человек", "мир", "материал", "час", "факт" } 

# Функция для извлечения данных и меток кластеров
def extract_data_and_labels(clustering: CLOPE.CLOPE, formatted_data):
    # Экстракция интересов и меток
    all_interests = set()
    for interests in formatted_data.values():
        all_interests.update(interests)

    # Создание матрицы для интересов
    data_matrix = np.zeros((len(formatted_data), len(all_interests)))
    interest_list = list(all_interests)
    
    for i, (user_id, interests) in enumerate(formatted_data.items()):
        for interest in interests:
            data_matrix[i, interest_list.index(interest)] = 1  # Устанавливаем 1, если интерес присутствует

    # Используйте словарь для хранения меток
    labels = {}
    for transaction_id, cluster_id in clustering.transaction.items():
        if transaction_id < len(formatted_data):
            labels[transaction_id] = cluster_id  # Присваиваем cluster_id по transaction_id
        else:
            print(f'Ошибка: transaction_id {transaction_id} выходит за пределы formatted_data')

    # Если нужно, вы можете создать список меток для совместимости с кодом, который ожидает список
    labels_list = [None] * len(formatted_data)
    for transaction_id, cluster_id in labels.items():
        labels_list[transaction_id] = cluster_id

    return data_matrix, labels_list


# Визуализация в 2D
def plot_clusters_with_interests(clustering: CLOPE.CLOPE, formatted_data):
    # Извлекаем данные и метки
    data_matrix, labels = extract_data_and_labels(clustering, formatted_data)

    # Применяем PCA для снижения размерности до 2
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data_matrix)

    # Определяем уникальные кластеры
    unique_labels = list(set(labels))

    plt.figure(figsize=(10, 8))
    
    # Отображаем точки, цветом соответствует кластерам
    for label in unique_labels:
        idx = [i for i, l in enumerate(labels) if l == label]
        plt.scatter(reduced_data[idx, 0], reduced_data[idx, 1], label=f'Cluster {label}')

    plt.title('Кластеры пользователей по интересам')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend()
    plt.grid()
    plt.show()


# 1. Визуализация количества транзакций по кластерам
def plot_transaction_counts(clustering):
    cluster_ids = list(clustering.clusters.keys())
    transaction_counts = [clustering.clusters[cluster_id].count_transactions*5 for cluster_id in cluster_ids]

    plt.figure(figsize=(10, 6))
    plt.bar(cluster_ids, transaction_counts, color='skyblue')
    plt.xlabel('ID Кластера')
    plt.ylabel('Количество пользователей')
    plt.title('Количество пользователей по кластерам')
    plt.xticks(cluster_ids)
    plt.grid(axis='y')
    plt.show()

# 2. Визуализация интересов по кластерам (если нужно)
def plot_interests(clustering: CLOPE.CLOPE, stop_words=None):
    if stop_words is None:
        stop_words = set()  # Пустое множество по умолчанию
    
    for cluster_id, cluster in clustering.clusters.items():
        interests = list(cluster.histogram.keys())
        counts = list(cluster.histogram.values())

        # Фильтруем стоп-слова и создаем словарь интересов
        filtered_interests = {}
        for interest, count in zip(interests, counts):
            if interest not in stop_words:
                filtered_interests[interest] = count

        # Сортируем по убыванию и берем топ-10
        sorted_interests = sorted(filtered_interests.items(), key=lambda item: item[1], reverse=True)[:10]

        if not sorted_interests:  # Если все интересы были в стоп-словах
            print(f"В кластере {cluster_id} все интересы были отфильтрованы как стоп-слова")
            continue

        top_interests, top_counts = zip(*sorted_interests)
        multiplied_counts = [count * 5 for count in top_counts]

        plt.figure(figsize=(10, 6))
        plt.bar(top_interests, multiplied_counts, color='lightgreen')
        
        plt.xlabel('Интересы')
        plt.ylabel('Количество')
        plt.title(f'Топ-10 интересов в кластере {cluster_id}')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

# Открываем JSON файл и читаем его содержимое
with open('src/data/users1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

formatted_data = {}
for entry in data:
    formatted_data[entry['id']] = [interest[0] for interest in entry['interests']]

# Инициализация параметров алгоритма
repulsion = 1.15
noiseLimit = 10
countTransfer = 1000000
stopLimit = 0
seed = 11465
seed1 = 57449

# Выполнение алгоритма
print('Start')
clope = CLOPE.CLOPE(print_step=1, random_seed=seed1)
clope.init_clusters(formatted_data, repulsion, noiseLimit)
print("Инициализация завершена. Число кластеров: ", len(clope.clusters))
clope.print_history_count(repulsion=repulsion, seed=clope.random_seed)
while countTransfer > stopLimit:
    countTransfer = clope.next_step(formatted_data, repulsion, noiseLimit)
    print("Число перемещений между кластерами", countTransfer, ". Число кластеров: ", len(clope.clusters))
    clope.print_history_count(repulsion=repulsion, seed=clope.random_seed)
print(clope.get_noise_limit())

# 2 д визуализация
# plot_clusters_with_interests(clope, formatted_data)

# Взываем функции для визуализации
plot_transaction_counts(clope)
plot_interests(clope, stop_words)


with open('src/data/CLOPE_users' + '.r=' + str(repulsion) + '.stopLimit=' + str(stopLimit) + '.pickle', 'wb') as f:
    pickle.dump(clope, f)