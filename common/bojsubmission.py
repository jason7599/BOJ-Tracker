from datetime import datetime
from dataclasses import dataclass

@dataclass
class BOJSubmission:
    username: str
    submit_id: int
    problem_id: int
    problem_title: str
    problem_href: str
    result_str: str
    submit_time: datetime