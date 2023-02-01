from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import List

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

vacancyLinks = ["https://gamedev.dou.ua/jobs/?category=Node.js", "https://gamedev.dou.ua/jobs/?category=Front+End"]


def get_vacancies_data(search_links: List[str]):
    names = []
    links = []
    company_names = []
    company_descriptions = []

    for searchedLink in search_links:
        driver.get(searchedLink)

        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")

        for a in soup.findAll('li', attrs={'class': 'l-vacancy'}):
            vacancy_name = a.find('a', attrs={'class': 'vt'}).contents[0]
            vacancy_link = a.find('a', attrs={'class': 'vt'})['href']
            vacancy_company_name = a.find('a', attrs={'class': 'company'}).contents[1]
            vacancy_company_description = a.find('div', attrs={'class': 'sh-info'}).contents[0]
            names.append(vacancy_name)
            links.append(vacancy_link)
            company_names.append(vacancy_company_name)
            company_descriptions.append(vacancy_company_description)

    df = pd.DataFrame({
        'Vacancy name': names,
        'Company name': company_names,
        # 'Description': company_descriptions,
        'Vacancy link': links
    })

    print(df.to_markdown())


get_vacancies_data(vacancyLinks)

