from algorithm.models.token_info import TokenInfo


class UserInfo:
    def __init__(self, id: int, interests: list[TokenInfo]):
        self.id = id
        self.interests = interests
    
    def to_dict(self):
        return {
            'id': int(self.id),
            'interests': self.interests
        }