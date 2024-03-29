import time
from aiocron import crontab
from typing import Optional
from pytz import BaseTzInfo
from pydantic import BaseModel, Field
from metagpt.schema import Message


class OssInfo(BaseModel):
    url: str
    timestamp: float = Field(default_factory=time.time)


class GithubTrendingCronTrigger():

    def __init__(self, spec: str, tz: Optional[BaseTzInfo] = None, url: str = "https://github.com/trending") -> None:
        self.crontab = crontab(spec, tz=tz)
        self.url = url

    def __aiter__(self):
        return self

    async def __anext__(self):
        await self.crontab.next()
        return Message(content=self.url, instruct_content=OssInfo(url=self.url))


if __name__ == '__main__':
    from pytz import timezone
    beijing_tz = timezone('Asia/Shanghai')  # 获取北京时间的时区
    cron_trigger = GithubTrendingCronTrigger("0 9 * * *", tz=beijing_tz)
