import json
import os
import numpy.random as nprnd
from algorithm.models.user_info import UserInfo
from algorithm.recommendation_algorithm import RecommendationAlgorithm

def get_random_users(n) -> list:
    return nprnd.randint(423307000, size=n)

def get_user_data(algorithm: RecommendationAlgorithm, user_id: int) -> UserInfo:
    print(f"Получение информации о пользователе с id = {user_id}")
    interests = algorithm.get_interests(user_id)
    if interests is None:
        print(f"Пользователь не найден, id = {user_id}")
        return None
    return UserInfo(user_id, interests)

def load_existing_data(filename: str):
    """Загружает существующие данные из файла или возвращает пустой список"""
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(filename: str, data: list):
    """Сохраняет данные в файл, перезаписывая его полностью"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def collect_data(filename: str, num_users: int = 100000):
    user_ids = get_random_users(num_users)
    algorithm = RecommendationAlgorithm()
    existing_data = load_existing_data(filename)
    existing_ids = {user['id'] for user in existing_data}
    
    count = 0
    index = 0
    new_users = []
    
    for user_id in user_ids:
        try:
            print(f"Итерация номер {index}, собранных пользователей: {count}")
            
            # Пропускаем уже существующих пользователей
            if user_id in existing_ids:
                print(f"Пользователь {user_id} уже есть в базе, пропускаем")
                continue
                
            user = get_user_data(algorithm, user_id)
            if user is None or len(user.interests) < 5:
                continue

            new_users.append(user.to_dict())
            existing_ids.add(user_id)
            count += 1
            print(f"Пользователь успешно записан, id: {user_id}")

        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            index += 1
            # Периодически сохраняем данные (каждые 2 пользователя)
            if count % 2 == 0 and new_users:
                combined_data = existing_data + new_users
                save_data(filename, combined_data)
                existing_data = combined_data.copy()
                new_users = []


filename = 'src/data/users.json'
collect_data(filename, num_users=100000)