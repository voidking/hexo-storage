from metagpt.roles import Role
from write_crawler_code import WriteCrawlerCode
from parse_sub_requirement import ParseSubRequirement

# 定义爬虫工程师角色


class CrawlerEngineer(Role):
    name: str = "John"
    profile: str = "Crawling Engineer"
    goal: str = "Write elegant, readable, extensible, efficient code"
    constraints: str = "The code should conform to standards like PEP8 and be modular and maintainable"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self._init_actions([WriteCrawlerCode])
        self._watch([ParseSubRequirement])
