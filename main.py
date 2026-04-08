import asyncio
from bot.growi_api import GrowiClient

async def main():
    client = GrowiClient("https://growi.maruru.me", "m9LQkGz4gm405Xql8KCDYFBwIXTnd+d/KWEiJ9qUMiM=")
    results = await client.get_growi_info("監視")
    for r in results:
        print(r["path"], r["url"])
    print(f"ヒット数: {len(results)}")


asyncio.run(main())