import requests
from bs4 import BeautifulSoup as bs
import json
import sqlite3

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
        # print(f"{ind}/{len(trs)}")

    return data



def get_recipe(category):
    data = {
        "category": category['category'],
        "recipes": []
    }
    print(f"Getting recipes for {category['category']}")
    for item in category['dishes']:
        r = requests.get(item['link'])
        soup = bs(r.content, 'lxml')
        ingredients = []
        trs = soup.find('table', {'class': 'mzr-recipe-view-ingredients'}).find('tbody').find_all("tr")
        for tr in trs:
            name = tr.find('td', {'class': 'el-name'})
            count = tr.find('td', {'class': 'el-count'})
            ingredients.append({
                'name': name.text,
                "count": count.text
            })
        recipe_desc = soup.find('p', {'itemprop': 'recipeInstructions'}).text
        recipe_desc = recipe_desc.replace("\n", "").strip().lstrip().rstrip()
        trs = soup.find('div', {'class': 'mzr-nutrition-value'}).find('tbody').find_all('tr')
        nutritional = []
        for tr in trs[1:]:
            tds = tr.find_all('td')
            n = tds[1].text
            v = tds[2].text
            nutritional.append({
                "name": n,
                "value": v
            })
        data['recipes'].append({
            'title': item['title'],
            'ingredients': ingredients,
            'recipe': recipe_desc,
            'nutritional': nutritional
        })
    return data


cats = get_categories()
for cat in cats:
    res = get_dishes_links(cat)
    r = get_recipe(res)
    with open(f"{cat['category']}.json", 'w+', encoding='utf-8') as f:
        json.dump(r, f, indent=4, ensure_ascii=False)
        f.close()
        
# for item in get_categories():
#     with open(f"{item['category']}.json", 'w+', encoding='utf-8') as f:
#         for i in get_dishes_links(item):
#             json.dump(get_recipe(i), f, indent=8, ensure_ascii=False)
#             f.close()