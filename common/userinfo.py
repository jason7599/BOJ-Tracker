from dataclasses import dataclass

@dataclass
class UserInfo:
    username: str
    last_submit_id: int # -1 indicates new

    def to_json(self):
        return {
            'name': self.username,
            'last_submit_id': self.last_submit_id
        }
    
    @staticmethod
    def from_json(json):
        return UserInfo(
            username=json['name'],
            last_submit_id=int(json['last_submit_id'])
        )