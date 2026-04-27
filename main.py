import os
import asyncio
import discord
from discord import app_commands
from bot.growi_api import GrowiClient
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.getenv("GROWI_URL")
token = os.getenv("GROWI_API_TOKEN")
discord_token = os.getenv("DISCORD_TOKEN")
if not url or not token or not discord_token:
    raise RuntimeError(
        "GROWI_URL / GROWI_API_TOKEN / DISCORD_TOKEN を .env に設定してください"
    )


growi = GrowiClient(url, token)

# Bot のセットアップ
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# 送信フォーマットを制定
async def send_results(interaction, keyword, results):
    item = f"{keyword}の検索結果{len(results)}件\n\n"
    for r in results:
        title = r["path"].split("/")[-1]
        line = f"📄 {title}\n{r['url']}\n\n"
        if len(item) + len(line) > 1900:
            await interaction.followup.send(item)
            item = ""
        item += line
    if item:
        await interaction.followup.send(item)


@tree.command(
    name="search_title",
    description="Growiのタイトルにその内容が含まれているかどうかを検索します",
)
async def title_search(interaction: discord.Interaction, keyword: str):
    if not growi.ready:
        await interaction.response.send_message("準備中です")
        return

    await interaction.response.defer()
    results = growi.search_title(keyword)
    if results:
        await send_results(interaction, keyword, results)
    else:
        await interaction.followup.send("1件もないです")


@tree.command(
    name="search_text",
    description="Growiの本文に単語が含まれているか確認します(時間がかかります)",
)
async def text_seatch(interaction: discord.Interaction, keyword: str):
    if not growi.ready:
        await interaction.response.send_message("準備中です")
        return

    await interaction.response.defer()
    results = growi.search_text(keyword)
    if results:
        await send_results(interaction, keyword, results)
    else:
        await interaction.followup.send("1件もないです")


@client.event
async def on_ready():
    await tree.sync()  # スラッシュコマンドを Discord に登録
    print(f"{client.user} としてログインしました")
    asyncio.create_task(growi.refresh_loop())


client.run(discord_token)
