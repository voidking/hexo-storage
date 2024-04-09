import datetime
from typing import Optional

from aiocron import crontab
from metagpt.schema import Message
from pytz import BaseTzInfo

# 触发器：crontab


class CronTrigger:
    def __init__(self, spec: str, tz: Optional[BaseTzInfo] = None) -> None:
        segs = spec.split(" ")
        if len(segs) == 6:
            spec = " ".join(segs[1:])
        self.crontab = crontab(spec, tz=tz)

    def __aiter__(self):
        return self

    async def __anext__(self):
        await self.crontab.next()
        return Message(datetime.datetime.now().isoformat())
