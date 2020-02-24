import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.103"
}

base_url = "https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=python&page=0"


def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, "lxml")

        try:
            num_of_pages = soup.find_all("a", attrs={"data-qa": "pager-page"})[-1].text
            num_of_pages = int(num_of_pages) + 1
            for i in range(num_of_pages):
                url = (
                    f"https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=python&page={i}")
                if url not in urls:
                    urls.append(url)
        except:
            pass

        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, "lxml")
            divs = soup.find_all("div", attrs={"data-qa": "vacancy-serp__vacancy"})
            for div in divs:
                try:
                    title = div.find("a", attrs={"data-qa": "vacancy-serp__vacancy-title"}).text
                    href = div.find("a", attrs={"data-qa": "vacancy-serp__vacancy-title"})['href']
                    company = div.find("a", attrs={"data-qa": "vacancy-serp__vacancy-employer"}).text
                    text_1 = div.find("div", attrs={"data-qa": "vacancy-serp__vacancy_snippet_responsibility"}).text
                    text_2 = div.find("div", attrs={"data-qa": "vacancy-serp__vacancy_snippet_requirement"}).text
                    descr = f"Ищем: {text_1}. Требования: {text_2}"
                    jobs.append({
                        'title': title,
                        'href': href,
                        'company': company,
                        'descr': descr
                    })
                    print('Спарсено количество вакансий: ', len(jobs))

                except:
                    pass

    else:
        print("Error!")
    print("Parsing finished!")
    return jobs


def write_jobs_to_file(jobs):
    with open('parsed jobs.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(('Вакансия', 'Ссылка', 'Компания', 'Описание'))
        for job in jobs:
            writer.writerow((job['title'], job['href'], job['company'], job['descr']))
        print("Writing to csv is finished!")


jobs = hh_parse(base_url, headers)

write_jobs_to_file(jobs)
