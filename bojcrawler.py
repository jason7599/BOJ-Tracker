import requests
from bs4 import BeautifulSoup
from datetime import datetime

INIT_SEARCH_URL = "https://www.acmicpc.net/status?problem_id=&user_id="
NEXT_PAGE_URL = "https://www.acmicpc.net"

class BOJSubmission:
    def __init__(self, problem_id: int, problem_title: str, result_str: str, submit_time: datetime):
        self.problem_id = problem_id
        self.problem_title = problem_title
        self.result_str = result_str
        self.submit_time = submit_time
    def __repr__(self):
        return f"BOJSubmission(problem_id={self.problem_id}, problem_title={self.problem_title}, result={self.result_str}, submit_time={self.submit_time})"

def crawl(user_id: str, max_cnt = 100, after_time = datetime.min) -> list[BOJSubmission]:

    url = INIT_SEARCH_URL + user_id

    res: list[BOJSubmission] = []

    while True:

        response = requests.get(url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" # not specifing a user agent causes a 403 Forbidden 
        })

        soup = BeautifulSoup(response.text, 'lxml')

        table_entries = soup.tbody.contents # list of tr tags
        
        done = False

        for entry in table_entries:

            problem_tag = entry.find(class_='problem_title')

            problem_id = problem_tag.string
            problem_title = problem_tag['title']

            result_str = entry.find(class_='result').string 
            submit_time = datetime.strptime(entry.find(class_='real-time-update')['title'],
                                             "%Y-%m-%d %H:%M:%S")

            if submit_time < after_time:
                done = True
                break

            submission = BOJSubmission(int(problem_id),
                                       problem_title,
                                       result_str,
                                       submit_time)

            res.append(submission)

            if len(res) == max_cnt:
                done = True
                break
        
        if done:
            break
        
        next_page_tag = soup.find('a', id='next_page')
        
        if not next_page_tag:
            break
    
        url = NEXT_PAGE_URL + next_page_tag['href']

    return res

submissions = crawl('shhhhzzang')

for submission in submissions:
    print(submission)
