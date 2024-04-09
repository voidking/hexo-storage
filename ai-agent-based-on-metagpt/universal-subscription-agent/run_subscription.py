import sys
from uuid import uuid4

from metagpt.actions.action import Action
from metagpt.tools.web_browser_engine import WebBrowserEngine
from trigger import CronTrigger
from metagpt.roles.role import Role
from metagpt.subscription import SubscriptionRunner

SUB_ACTION_TEMPLATE = """
## Requirements
Answer the question based on the provided context {process}. If the question cannot be answered, please summarize the context.

## context
{data}"
"""

# 运行订阅智能体的Action


class RunSubscription(Action):
    async def run(self, msgs):
        code = msgs[-1].content
        req = msgs[-2].instruct_content.dict()
        urls = req["Crawler URL List"]
        process = req["Crawl Post Processing"]
        spec = req["Cron Expression"]
        SubAction = self.create_sub_action_cls(urls, code, process)
        SubRole = type("SubRole", (Role,), {})
        role = SubRole()
        role._init_actions([SubAction])
        runner = SubscriptionRunner()

        async def callback(msg):
            print(msg)

        await runner.subscribe(role, CronTrigger(spec), callback)
        await runner.run()

    @staticmethod
    def create_sub_action_cls(urls: list[str], code: str, process: str):
        modules = {}
        for url in urls[::-1]:
            code, current = code.rsplit(f"# {url}", maxsplit=1)
            name = uuid4().hex
            module = type(sys)(name)
            exec(current, module.__dict__)
            modules[url] = module

        class SubAction(Action):
            async def run(self, *args, **kwargs):
                pages = await WebBrowserEngine().run(*urls)
                if len(urls) == 1:
                    pages = [pages]

                data = []
                for url, page in zip(urls, pages):
                    data.append(getattr(modules[url], "parse")(page.soup))
                return await self.llm.aask(SUB_ACTION_TEMPLATE.format(process=process, data=data))

        return SubAction
