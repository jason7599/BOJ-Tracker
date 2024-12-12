from datetime import datetime
from dataclasses import dataclass

@dataclass
class BOJSubmission:
    username: str
    problem_title: str
    problem_href: str
    result_str: str
    submit_time: datetime

    def to_json(self):
        return {
            'username': self.username,
            'problem_title': self.problem_title,
            'problem_href': self.problem_href,
            'result': self.result_str,
            'time': self.submit_time.isoformat()
        }
    
    @staticmethod
    def from_json(json):
        return BOJSubmission(
            username=json['username'],
            problem_title=json['problem_title'],
            problem_href=json['problem_href'],
            result_str=json['result'],
            submit_time=datetime.fromisoformat(json['time']),
        )