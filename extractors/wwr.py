from requests import get
from bs4 import BeautifulSoup

# base_url = "https://weworkremotely.com/remote-jobs/search?&term="

# search_term = "python"

# response = get(f"{base_url}{search_term}")
# if response.status_code != 200:
#     print("can't request website")
# else:
#     results = []
#     soup = BeautifulSoup(response.text, "html.parser")
#     # _쓰는 이유: class라는 단어를 python이 사용중이라
#     jobs = soup.find_all('section', class_="jobs")
#     for job_section in jobs:
#         job_posts = job_section.find_all('li')
#         job_posts.pop(-1)  # .=list
#         for post in job_posts:
#             anchors = post.find_all('a')
#             anchor = anchors[1]
#             link = anchor['href']
#             company, kind, region = anchor.find_all(
#                 'span', class_="company")
#             # find_all list를 가져오고, find는 결과를 가져온다.
#             title = anchor.find('span', class_='title')
#             job_date = {
#                 'link': f"https://weworkremotely.com{link}",
#                 'company': company.string,
#                 'region': region.string,
#                 'position': title.string
#             }
#             results.append(job_date)
#     for result in results:
#       print(result)
#       print("///////")


def extract_wwr_jobs(keyword):  # function 사용시 define 안에 있어야함

    base_url = "https://weworkremotely.com/remote-jobs/search?&term="

    search_term = "python"

    response = get(f"{base_url}{search_term}")
    if response.status_code != 200:
        print("can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        # _쓰는 이유: class라는 단어를 python이 사용중이라
        jobs = soup.find_all('section', class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)  # .=list
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = anchor['href']
                company, title, region = anchor.find_all(
                    'span', class_="company")
                # find_all list를 가져오고, find는 결과를 가져온다.
                title = anchor.find('span', class_='title')
                job_date = {
                    'link': f"https://weworkremotely.com{link}",
                    'company': company.string,
                    'location': region.string,
                    'position': title.string
                }
                results.append(job_date)
        return results
