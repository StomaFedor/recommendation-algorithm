import requests

from algorithm.models.group_info import GroupInfo

class VkApiClient:
    tokens = ["",
              ""]
    token_index = 0
    max_token_count = len(tokens)

    
    def get_user_groups(self, user_id) -> list:
        response = requests.get('https://api.vk.com/method/users.getSubscriptions', params={
            'access_token': self.tokens[self.token_index],
            'user_id': user_id,
            'v': 5.199,
        })
        data = response.json()

        if response.status_code != 200 or 'error' in data:
            if data['error']['error_code'] == 29 or data['error']['error_code'] == 5:
                self.token_index += 1
                
            print("Ошибка при запросе получения групп пользователя, user_id = " + str(user_id) 
                  + "; token_index = " + str(self.token_index)
                   + "; response = " + data['error']['error_msg'])
            return
        
        groups = []
        
        group_items = data['response']['groups']['items']
        groups.extend(group_items)

        return groups
    
    def get_group_info(self, group_id) -> GroupInfo:
        response = requests.get('https://api.vk.com/method/groups.getById', params={
            'access_token': self.tokens[self.token_index],
            'group_id': group_id,
            'v': 5.199,
            'fields': "description",
        })
        data = response.json()

        if response.status_code != 200 or 'error' in data:
            if data['error']['error_code'] == 29 or data['error']['error_code'] == 5:
                self.token_index += 1
            print("Ошибка при запросе получения информации о группе, group_id = " + str(group_id)
                  + "; token_index = " + str(self.token_index)
                  + "; response = " + data['error']['error_msg'])
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