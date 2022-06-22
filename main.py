import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def extract(job, page):
    global job_title
    job_title = job
    url = f'https://uk.indeed.com/jobs?q={job}&l=London%2C%20Greater%20London&start={page}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/101.0.4951.54 Safari/537.36'}
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    jobs = soup.find_all('div', class_='job_seen_beacon')
    nu_of_jobs = soup.find('div', {'id': 'searchCountPages'}).text.strip()
    nu_of_jobs = re.sub('[Page, fjbs]', '', nu_of_jobs)
    noj_list = nu_of_jobs.split('o')
    noj_list.pop(0)
    noj_list.pop(-1)
    nu_of_jobs = noj_list[0]
    summary = 0
    counter = 0
    for item in jobs:
        try:
            salary = item.find('div', class_='attribute_snippet').text.strip()
            salary = re.sub('[FromUpt\-yea ,]', '', salary)
            salary_list = salary.split("£")
            salary_list.pop(0)
            if len(salary_list) >= 2:
                salary_list.pop(-1)
            temp_salary_store = int(salary_list[0])
            summary += temp_salary_store
            counter += 1
        except:
            salary = ''
    summary /= counter
    # queried_list.append(advert)
    advert = {
        'Title': job_title,
        'Number of Jobs': nu_of_jobs,
        'Average Salary': summary
    }
    return advert

# queried_list = []



# for i in range(0, 40, 10):
#     print(f'Getting page {i/10+1}')
print(transform(extract('Junior Python Developer', 0)))

# df = pd.DataFrame(queried_list)
# print(df.head())
# df.to_csv('jobs.csv')