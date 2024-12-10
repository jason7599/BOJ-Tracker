from datetime import datetime

class BOJSubmission:
    def __init__(self, submit_id: int, problem_id: int, problem_title: str, problem_href: str, result_str: str, submit_time: datetime):
        self.submit_id = submit_id
        self.problem_id = problem_id
        self.problem_title = problem_title
        self.problem_href = problem_href
        self.result_str = result_str
        self.submit_time = submit_time
    def __repr__(self):
        return f"BOJSubmission(problem_id={self.problem_id}, problem_title={self.problem_title}, result={self.result_str}, submit_time={self.submit_time})"