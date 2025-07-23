from algorithm.vk_api_client import VkApiClient
from algorithm.lemmatizer import Lemmatizer
import operator

class RecommendationAlgorithm:
    def __init__(self):
        self.vk_api = VkApiClient()
        self.lemm = Lemmatizer()

    def get_interests(self, user_id: int) -> list:
        group_ids = self.vk_api.get_user_groups(user_id)
        if group_ids == None:
            return

        token_dict = dict()
        for group_id in group_ids:
            group_info = self.vk_api.get_group_info(group_id)
            if group_info == None:
                continue
            tokens = self.lemm.lemmatize(group_info.name + " " +  group_info.description)
            if tokens == None:
                continue

            for token in tokens:
                if token not in token_dict:
                    token_dict[token] = 0
                token_dict[token] += 1

        sorted_tokens = sorted(token_dict.items(), key=operator.itemgetter(1), reverse=True)

        top_tokens = sorted_tokens[:5]
        return top_tokens

    def get_recommendations(self, user_id: int) -> list:
        top_tokens = self.get_interests(user_id)

        result_ids = []
        for token in top_tokens:
            group_ids = self.vk_api.search_group(token[0])
            for group_id in group_ids:
                if group_id not in result_ids:
                    result_ids.append(group_id)
                    break

        result_links = []
        for id in result_ids:
            result_links.append("https://vk.com/public" + str(id))
        
        return result_links