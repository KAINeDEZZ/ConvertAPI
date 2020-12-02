from aiohttp import ClientSession, ClientTimeout, client_exceptions
import exceptions
from lxml import html

CBR_URL = 'https://www.cbr.ru/currency_base/daily/'


async def parse_table() -> dict or Exception:
    client = ClientSession(timeout=ClientTimeout(2))

    try:
        response = await client.get(CBR_URL)

        data = {}
        if response.status == 200:
            doc = html.document_fromstring(await response.text())

            for line in doc.xpath('//tr/td/parent::*'):
                cells = line.getchildren()
                data[cells[1].text] = float(cells[4].text.replace(',', '.')) / int(cells[2].text)

    except client_exceptions.ClientConnectionError:
        return exceptions.GetTableFromWebException()

    except Exception as ex:
        return ex

    finally:
        await client.close()

    if data:
        return data
    else:
        return exceptions.ParseException()
