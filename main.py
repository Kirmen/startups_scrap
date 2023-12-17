import json
import os

from bs4 import BeautifulSoup
import requests


def get_data(url):
    if os.path.exists('data'):
        print('"data" already exists')
    else:
        os.mkdir('data')

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.5414.120 Safari/537.36 Avast/109.0.19987.120'
    }

    req = requests.get(url, headers=headers)
    with open('all_projects.html', 'wb') as file:
        file.write(req.content)

    with open('all_projects.html', 'r', encoding='UTF-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    a_tags = soup.find_all('a', class_='projects_list_b')

    project_names = []
    all_hrefs = []

    final_projects_list = []

    for a in a_tags:
        project_names.append(a.find('div', class_='title').text)
        all_hrefs.append(a.get('href'))

    projects_n_url = dict(zip(project_names, all_hrefs))

    for project_name, project_url in projects_n_url.items():
        req = requests.get(project_url, headers=headers)

        with open(f'data/{project_name}.html', 'wb') as file:
            file.write(req.content)

        with open(f'data/{project_name}.html', 'r', encoding='UTF-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        short_d = soup.find('div', class_='main_d').find_all('span')

        try:
            short_description = short_d[0].text
        except Exception:
            short_description = 'has not short description'
        try:
            tags = short_d[2].text.split(',')
        except Exception:
            tags = 'has not a tags'
        try:
            full_description = soup.find('span', itemprop='description').text
        except Exception:
            full_description = 'has not full description'
        try:
            pic = soup.find('img', itemprop='image').get('src')
        except Exception:
            pic = 'Has not a pic'

        final_projects_list.append({
            'Name': project_name,
            'Short description': short_description,
            'Tags': tags,
            'Description': full_description,
            'Pictur\'s URL': pic,
            'URL': project_url
        })

    with open(f'data/startups.json', 'a', encoding='UTF-8') as file:
        json.dump(final_projects_list, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    url = 'https://startup.ua/ua/startups/'
    get_data(url)
