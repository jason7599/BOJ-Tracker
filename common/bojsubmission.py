from datetime import datetime
from dataclasses import dataclass

from common.submissionresult import SubmissionResult

@dataclass
class BOJSubmission:
    username: str
    submit_id: int
    problem_title: str
    problem_href: str
    result: SubmissionResult
    submit_time: datetime

    def to_json(self):
        return {
            'username': self.username,
            'submit_id': self.submit_id,
            'problem_title': self.problem_title,
            'problem_href': self.problem_href,
            'result': self.result.to_json(),
            'time': self.submit_time.isoformat()
        }
    
    @staticmethod
    def from_json(json):
        return BOJSubmission(
            username=json['username'],
            submit_id=int(json['submit_id']),
            problem_title=json['problem_title'],
            problem_href=json['problem_href'],
            result=SubmissionResult.from_json(json['result']),
            submit_time=datetime.fromisoformat(json['time']),
        )