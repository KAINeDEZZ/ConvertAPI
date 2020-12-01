from aiohttp import ClientSession
from lxml import html
from typing import List

CBR_URL = 'https://www.cbr.ru/currency_base/daily/'


class Currency:
    def __init__(self, code: str, cost: float):
        self.code = code
        self.cost = cost


async def get_table() -> List[Currency]:
    client = ClientSession()
    response = await client.get(CBR_URL)
    doc = html.document_fromstring(await response.text())

    data = []
    for line in doc.xpath('//tr/td/parent::*'):
        cells = line.getchildren()
        data.append(Currency(cells[1].text, float(cells[4].text.replace(',', '.')) / int(cells[2].text)))

    await client.close()
    return data
