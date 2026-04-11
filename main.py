import os
import discord
from discord import app_commands
from bot.growi_api import GrowiClient
from dotenv import load_dotenv

load_dotenv(override=True)

growi = GrowiClient(os.getenv("GROWI_URL"),os.getenv("GROWI_API_TOKEN"))

# Bot のセットアップ
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="search", description="Growiのタイトルにその内容が含まれているかどうかを検索します")
async def search(interaction: discord.Interaction, keyword: str):
    
    await interaction.response.send_message(f"{keyword} で検索中...")
    results = await growi.get_growi_info(keyword)
    if not results:
        await interaction.followup.send("検索結果が見つかりませんでした")
        return
    message = f"「{keyword}」の検索結果（{len(results)}件）\n\n"
    for r in results[:5]:
        title = r["path"].split("/")[-1]
        message += f"📄 {title}\n{r['url']}\n\n"
    if len(results) > 5:
        message += f"...他 {len(results) - 5} 件"
    await interaction.followup.send(message)
        
@client.event
async def on_ready():
    await tree.sync()  # スラッシュコマンドを Discord に登録
    print(f"{client.user} としてログインしました")

client.run(os.getenv("DISCORD_TOKEN"))