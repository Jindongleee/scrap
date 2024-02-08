from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from extractors.wwr import extract_wwr_jobs


def get_page_count(keyword):

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # from folder.file import function name
    # import시 pyc 파일 생성

    browser = webdriver.Chrome(options=options)

    base_url = "https://kr.indeed.com/jobs?q="

    browser.get(f"{base_url}{keyword}")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", class_="ecydgvn0")
    if pagination == None:
        return 1
    pages = pagination.find_all("div", recursive=False)
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(options=options)

        base_url = "https://kr.indeed.com/jobs"

        final_url = (f"{base_url}?q={keyword}&start={page*10}")

        print("Requesting", final_url)
        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")  # h2에 있는 a를 가져와라
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    'link': f"https://www.indeed.com{link}",
                    'company': company.string,
                    'location': location.string,
                    'position': title
                }
                results.append(job_data)
    return results


jobs = extract_wwr_jobs("python")
print((jobs))

# None #있어야하는데 없을때
# recursive = False 바로 아래만 찾아줌
# mosaic zone까지 바로 포함되는 문제점있음
