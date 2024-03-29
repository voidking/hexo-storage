import asyncio

from metagpt.schema import Message
from metagpt.subscription import SubscriptionRunner
from oss_watcher import OssWatcher
from trigger import GithubTrendingCronTrigger
from pusher import push_to_discord, push_to_wechat


async def main(spec: str = "0 9 * * *", discord: bool = True, wxpusher: bool = True):
    callbacks = []
    if discord:
        callbacks.append(push_to_discord)

    if wxpusher:
        callbacks.append(push_to_wechat)

    if not callbacks:
        async def _print(msg: Message):
            print(msg.content)
        callbacks.append(_print)

    async def callback(msg):
        await asyncio.gather(*(call(msg) for call in callbacks))

    runner = SubscriptionRunner()
    await runner.subscribe(OssWatcher(), GithubTrendingCronTrigger(spec), callback)
    await runner.run()


if __name__ == "__main__":
    import fire
    # fire.Fire(main)
    fire.Fire(lambda: asyncio.run(main(spec="* * * * *", discord=False, wxpusher=True)))
