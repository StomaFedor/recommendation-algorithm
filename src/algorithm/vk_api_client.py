import requests

from algorithm.group_info import GroupInfo

class VkApiClient:
    token = ""
    
    def get_user_groups(self, user_id) -> list:
        response = requests.get('https://api.vk.com/method/users.getSubscriptions', params={
            'access_token': self.token,
            'user_id': user_id,
            'v': 5.199,
        })
        if response.status_code != 200:
            print("Ошибка при запросе получения групп пользователя, user_id = " + str(user_id))
            return
        
        groups = []
        data = response.json()
        if 'error' in data:
            print("Ошибка при запросе получения групп пользователя, пользователь не найден, user_id = " + str(user_id))
            return
        
        group_items = data['response']['groups']['items']
        groups.extend(group_items)

        return groups
    
    def get_group_info(self, group_id) -> GroupInfo:
        response = requests.get('https://api.vk.com/method/groups.getById', params={
            'access_token': self.token,
            'group_id': group_id,
            'v': 5.199,
            'fields': "description",
        })
        if response.status_code != 200:
            print("Ошибка при запросе получения информации о группе, group_id = " + str(group_id))
            return
        
        data = response.json()
        if 'error' in data:
            print("Ошибка при запросе получения информации о группе, группа не найдена, group_id = " + str(group_id))
            return

        group_info_dict = data['response']['groups'][0]
        if group_info_dict['is_closed'] == 2:
            return
        
        group_info = GroupInfo(group_info_dict['name'], group_info_dict['description'])

        return group_info
    
    def search_group(self, search_text) -> list:
        response = requests.get('https://api.vk.com/method/groups.search', params={
            'access_token': self.token,
            'q': search_text,
            'v': 5.199,
            'count': 5,
        })
        if response.status_code != 200:
            print("Ошибка при запросе поиска группы, search_text = " + search_text)
            return
        
        data = response.json()
        if 'error' in data:
            print("Ошибка при запросе поиска группы, search_text = " + search_text)
            return
        
        items = data['response']['items'][:5]

        group_ids = []
        for item in items:
            group_ids.append(item['id'])

        return group_ids