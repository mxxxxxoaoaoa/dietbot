import requests
from bs4 import BeautifulSoup as bs
import json

def get_categories():
    r = requests.get("https://health-diet.ru/base_of_meals/")
    soup = bs(r.content, 'lxml')
    grid = soup.find("div", {'class': 'uk-grid uk-grid-medium'})
    cgrid = grid.find_all('div', {'class': 'uk-width-1-1 uk-width-small-1-1 uk-width-medium-1-2 uk-width-large-1-2'})
    data = []
    for c in cgrid:
        cdiv = c.find_all("div", {'class': 'uk-flex mzr-tc-group-item'})
        for div in cdiv:
            tmp = div.find('a')
            data.append({
                "category": tmp.text,
                "link": 'https://health-diet.ru' + tmp['href']
            })
    return data

def get_dishes_links(category):
    r = requests.get(category['link'])
    soup = bs(r.content, 'lxml')
    table = soup.find("table", {'class': 'uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed'}).find("tbody")
    trs = table.find_all('tr')
    data = {
        "category": category['category'],
        "dishes": []
    }
    print(f"Getting {category['category']}")
    for ind, tr in enumerate(trs):
        tmp = tr.find('td').find("a")
        data['dishes'].append({
            "title": tmp['title'].split(":")[1].strip(),
            "link": "https://health-diet.ru" + tmp['href']
        })
        print(f"{ind}/{len(trs)}")

    return data

# for item in get_categories():
#     with open(f"{item['category']}.json", 'w+', encoding='utf-8') as f:
#         json.dump(get_dishes_links(item), f, indent=8, ensure_ascii=False)
#         f.close()