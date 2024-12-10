import requests
from bs4 import BeautifulSoup
from datetime import datetime

from common.bojsubmission import BOJSubmission

# not specifing a user agent causes a 403 Forbidden
REQUEST_HEADERS = \
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
}

USER_SEARCH_URL = "https://www.acmicpc.net/user/"
INIT_SEARCH_URL = "https://www.acmicpc.net/status?problem_id=&user_id="
BOJ_BASE_URL = "https://www.acmicpc.net"

SUBMIT_TAG_ID_PREFIX = "solution-"


def boj_user_exists(username: str) -> bool:
    response = requests.get(USER_SEARCH_URL + username, headers=REQUEST_HEADERS)
    return response.status_code == 200


def boj_get_submissions(username: str, max_cnt = 100, after_time = datetime.min) -> list[BOJSubmission]:

    url = INIT_SEARCH_URL + username

    res: list[BOJSubmission] = []

    while True:

        response = requests.get(url, headers=REQUEST_HEADERS)

        # probably would never happen unless BOJ relocates their URL
        # if this happens at all, it would be on the first search,
        # as even inputting a non-existent username does come back with status code 200.
        if response.status_code != 200:
            raise Exception(f"Request on {url} returned with code {response.status_code}!")

        # lxml parser
        soup = BeautifulSoup(response.text, 'lxml')

        table_entries = soup.tbody.contents # list of tr tags
        
        done = False

        for entry in table_entries:

            submit_time = datetime.strptime(entry.find(class_='real-time-update')['title'],
                                             "%Y-%m-%d %H:%M:%S")

            if submit_time < after_time:
                done = True
                break

            submit_id = int(entry['id'].removeprefix(SUBMIT_TAG_ID_PREFIX))

            problem_tag = entry.find(class_='problem_title')

            problem_id = int(problem_tag.string)
            problem_title = problem_tag['title']
            problem_href = BOJ_BASE_URL + problem_tag['href']

            result_str = entry.find(class_='result').string 

            submission = BOJSubmission(username,
                                       submit_id,
                                       problem_title,
                                       problem_href,
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
    
        url = BOJ_BASE_URL + next_page_tag['href']

    return res