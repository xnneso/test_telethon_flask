from urllib.parse import urlencode
from requests import get


"""Не стал усложнять функцию всякими хедерами/агентами для запроса, запрос ниже прекрасно отрабатывает"""
def parse_wb():
    params = {
        'curr': 'rub',
        'query': 'любой товар',
        'dest': -1257786,
        'limit': 10,
        'resultset': 'catalog',
    }
    query = urlencode(params)
    try:
        response = get(f'https://search.wb.ru/exactmatch/ru/common/v5/search?{query}').json()
    except:
        return {'result': 'error'}
    result = []
    for i in response['data']['products']:
        result.append(
            {'name': i['name'], 'link': f'https://www.wildberries.ru/catalog/{i["id"]}/detail.aspx'})
    return result
