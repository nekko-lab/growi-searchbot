import aiohttp
import asyncio
from urllib.parse import quote


class GrowiClient:
    def __init__(self, url: str, access_token: str):
        self.url = url
        self.access_token = access_token
        self.pages = []
        self.ready = False

    # すべてのページのタイトルとURLを取得する関数
    async def fetch_all_pages(self) -> list[dict]:
        id_get = f"{self.url}/_api/v3/pages/list"
        id_params = {
            "access_token": (self.access_token),
            "path": "/",
            "page": 1,
        }
        text_get = f"{self.url}/_api/v3/page"
        async with aiohttp.ClientSession() as session:
            all_pages = []
            while True:
                async with session.get(id_get, params=id_params) as res:
                    data = await res.json()
                    pages = data["pages"]
                    for page in pages:
                        all_pages.append(page)
                    if len(pages) < 20:
                        break
                    id_params["page"] += 1

            async def fetch_body(page):
                text_params = {
                    "access_token": self.access_token,
                    "pageId": page["_id"],
                }
                async with session.get(text_get, params=text_params) as res:
                    data = await res.json()
                    return {
                        "path": page["path"],
                        "body": data["page"]["revision"]["body"],
                        "url": f"{self.url}{quote(page['path'])}",
                    }

            tasks = [fetch_body(p) for p in all_pages]
            results = await asyncio.gather(*tasks)
            return results

    # fetch_all_pagesを呼び出すためだけの関数
    async def refresh(self):
        new_pages = await self.fetch_all_pages()
        self.pages = new_pages
        self.ready = True

    # 一時間ごとにページを更新する

    async def refresh_loop(self):
        while True:
            try:
                await self.refresh()
            except Exception as e:
                print(f"error:{e}")
            await asyncio.sleep(3600)

    # タイトルから検索する
    def search_title(self, keyword: str) -> list[dict]:
        results = []
        for i in self.pages:
            if keyword in i["path"]:
                results.append(i)
        return results

    # 本文から検索する
    def search_text(self, keyword: str) -> list[dict]:
        results = []
        for i in self.pages:
            if keyword in i["body"]:
                results.append(i)
        return results
