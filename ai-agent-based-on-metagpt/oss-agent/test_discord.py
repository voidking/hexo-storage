import os
import asyncio
import discord

# 注意：中国大陆地区无法访问Discord，使用代理也不行，暂未找到解决办法


async def push_to_discord():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    # client = discord.Client(intents=intents, proxy='http://127.0.0.1:7890')
    token = os.environ["DISCORD_TOKEN"]
    channel_id = int(os.environ["DISCORD_CHANNEL_ID"])
    async with client:
        await client.login(token)
        channel = await client.fetch_channel(channel_id)
        await channel.send("test")

result = asyncio.run(push_to_discord())
print(result)
