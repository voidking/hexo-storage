#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import asyncio
import aiohttp
from typing import Optional

import discord

from metagpt.config import CONFIG
from metagpt.schema import Message

# 定义Discord Pusher


async def push_to_discord(msg: Message):
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents, proxy=CONFIG.global_proxy)
    # client = discord.Client(intents=intents, proxy='http://127.0.0.1:7890')
    token = os.environ["DISCORD_TOKEN"]
    channel_id = int(os.environ["DISCORD_CHANNEL_ID"])
    async with client:
        await client.login(token)
        channel = await client.fetch_channel(channel_id)
        lines = []
        for i in msg.content.splitlines():
            if i.startswith(("# ", "## ", "### ")):
                if lines:
                    await channel.send("\n".join(lines))
                    lines = []
            lines.append(i)

        if lines:
            await channel.send("\n".join(lines))


class WxPusherClient:
    def __init__(self, token: Optional[str] = None, base_url: str = "http://wxpusher.zjiecode.com"):
        self.base_url = base_url
        self.token = token or os.environ["WXPUSHER_TOKEN"]

    async def send_message(
        self,
        content,
        summary: Optional[str] = None,
        content_type: int = 1,
        topic_ids: Optional[list[int]] = None,
        uids: Optional[list[int]] = None,
        verify: bool = False,
        url: Optional[str] = None,
    ):
        payload = {
            "appToken": self.token,
            "content": content,
            "summary": summary,
            "contentType": content_type,
            "topicIds": topic_ids or [],
            "uids": uids or os.environ["WXPUSHER_UIDS"].split(","),
            "verifyPay": verify,
            "url": url,
        }
        url = f"{self.base_url}/api/send/message"
        return await self._request("POST", url, json=payload)

    async def _request(self, method, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()

# 定义Wechat Pusher


async def push_to_wechat(msg: Message):
    client = WxPusherClient()
    await client.send_message(msg.content, content_type=3)

if __name__ == '__main__':
    result = asyncio.run(push_to_wechat(Message("test")))
