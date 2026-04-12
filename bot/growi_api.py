import aiohttp
import asyncio
from urllib.parse import quote
class GrowiClient:
    def __init__(self,url: str,access_token: str):
        self.url = url
        self.access_token = access_token
    
    async def get_growi_title(self,keyword: str)->list[dict]:
        #エンドポイントの作成
        apiEndPoint = f'{self.url}/_api/v3/pages/list'
        params = {
            'access_token': (self.access_token),
            'path': '/',
            'page': 1,
        }
        #非同期で取れるようにする
        results = []
        async with aiohttp.ClientSession() as session:
            while(True):
              async with session.get(apiEndPoint,params=params) as res:
                    data = await res.json()
                    pages = data["pages"]
                    for page in pages:
                        if keyword in page["path"]:
                            results.append({
                                "path": page["path"],
                                "url": f"{self.url}{quote(page['path'])}",
                            })
                    if len(pages) < 20:
                        break
                    params["page"] += 1
        return results
    async def get_growi_text(self,keyword: str)->list[dict]:
        results = []
        id_get = f'{self.url}/_api/v3/pages/list'
        id_params = {
            'access_token': (self.access_token),
            'path': '/',
            'page': 1,
        }
        text_get = f'{self.url}/_api/v3/page'
        async with aiohttp.ClientSession() as session:
            all_pages = []
            while(True):
                async with session.get(id_get,params=id_params) as res:
                    data = await res.json()
                    pages = data["pages"]
                    for page in pages:
                        all_pages.append(page)
                    if len(pages) < 20:
                        break
                    id_params["page"] += 1
            async def fetch_body(page):
                text_params = {
                   'access_token': self.access_token,
                   'pageId': page['_id'],
                }
                async with session.get(text_get, params=text_params) as res:
                    data = await res.json()
                    body = data["page"]["revision"]["body"]
                    if keyword in body:
                        return({
                            "path": page["path"],
                            "url": f"{self.url}{quote(page['path'])}",
                    })
                return None
            
            tasks =  [fetch_body(page) for page in all_pages]
            results_raw = await asyncio.gather(*tasks)
            results = [r for r in results_raw if r is not None]
        return results
    
